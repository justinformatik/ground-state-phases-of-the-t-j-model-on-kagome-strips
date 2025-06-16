using ITensors
using LinearAlgebra
using CSV
using DataFrames
using Random
using Plots

# This code generates all data for the kagome strips. Parameters and the directory can be changed in the main() function. 
#number_of_bonds = 10 + 12 * (stars - 1)

function hexagon_strip_top_triangles_neighbors_connected_fully(stars)
    neighbors = Dict{Int, Vector{Int}}()
    deleted_vertices = []  # list of overlapping indices
    vertices_per_hex = 8   # There are 8 vertices in each star 
    # Create stars (hexagons plus triangles)
    for hex_in_row in 1:stars
        base_index = (hex_in_row - 1) * vertices_per_hex + 1  # Base index of the current hexagon
        for v in 1:vertices_per_hex
            current_vertex = base_index + v - 1  # Index of the current vertex
            neighbors_list = []

            if v <= 6  # hexagon structure
                prev_vertex = (v == 1) ? (base_index + 5) : (current_vertex - 1)
                next_vertex = (v == 6) ? base_index : (current_vertex + 1)
                neighbors_list = [prev_vertex, next_vertex]

            elseif v == 7  # adding top triangle
                # Vertex 7 connects to vertices 2 and 3
                neighbors_list = [base_index + 1, base_index + 2]
                push!(neighbors[base_index + 1], current_vertex)
                push!(neighbors[base_index + 2], current_vertex)  # bidirectional connection

            elseif v == 8  # adding bottom triangle
                # Vertex 8 connects to vertices 4 and 5
                neighbors_list = [base_index + 4, base_index + 5]
                push!(neighbors[base_index + 4], current_vertex)
                push!(neighbors[base_index + 5], current_vertex)  # bidirectional connection
            end
            neighbors[current_vertex] = neighbors_list
        end
    end

    # Connect stars
    for hex_in_row in 2:stars 
        base_index = (hex_in_row - 1) * vertices_per_hex + 1

        # Connect v == 4 of the current hexagon with v == 1 of the previous hexagon
        current_vertex_3 = base_index + 3
        prev_hex_vertex_6 = base_index - vertices_per_hex  # + 5

        # Merge the neighbors of the current vertex with the previous hexagons vertex
        neighbors[prev_hex_vertex_6] = unique(vcat(neighbors[prev_hex_vertex_6], neighbors[current_vertex_3]))

        # Remove the current vertex 
        for neighbor in neighbors[current_vertex_3]
            replace!(neighbors[neighbor], current_vertex_3 => prev_hex_vertex_6)
        end
        delete!(neighbors, current_vertex_3)
        push!(deleted_vertices, current_vertex_3)  # Add to deleted vertices

        # Connect v == 3 of the current hexagon with v == 2 of the previous hexagon
        current_vertex_2 = base_index + 2
        prev_hex_vertex_1 = base_index - vertices_per_hex + 1

        push!(neighbors[current_vertex_2], prev_hex_vertex_1)
        push!(neighbors[prev_hex_vertex_1], current_vertex_2)

        # Connect v == 5 of the current hexagon with v == 6 of the previous hexagon
        current_vertex_4 = base_index + 4
        prev_hex_vertex_5 = base_index - vertices_per_hex + 5

        push!(neighbors[current_vertex_4], prev_hex_vertex_5)
        push!(neighbors[prev_hex_vertex_5], current_vertex_4)
    end
    return neighbors, deleted_vertices
end

function renumber(neighbors, deleted_vertices) # ensures that all indices are existent for MPS
    new_neighbors = Dict{Int, Vector{Int}}()
    biggest_key = maximum(keys(neighbors))

    renumber_map = Dict{Int, Int}()
    new_index = 1

    for i in 1:biggest_key
        if i in deleted_vertices
            continue
        else
            renumber_map[i] = new_index
            new_index += 1
        end
    end

    for (old_index, neighbor_list) in neighbors
        if haskey(renumber_map, old_index)
            new_index = renumber_map[old_index]
            new_neighbor_list = [renumber_map[neighbor] for neighbor in neighbor_list if haskey(renumber_map, neighbor)]
            new_neighbors[new_index] = new_neighbor_list
        end
    end
    return new_neighbors
end

function map_neighbors_to_bonds(neighbors)
    bond_dict = Dict{Int, Tuple{Int, Int}}()
    bond_set = Set{Tuple{Int, Int}}() 
    bond_index = 1

    for (vertex, neighbor_list) in neighbors
        for neighbor in neighbor_list
            bond = (vertex < neighbor) ? (vertex, neighbor) : (neighbor, vertex) 
            if !in(bond, bond_set)
                push!(bond_set, bond)
                bond_dict[bond_index] = bond
                bond_index += 1
            end
        end
    end
    return bond_dict
end
### all functions above can be exchanged with the neighbor functions for the chain to generate all data for the chain

function create_random_initial_state(filled_spots, N) # creates a random inital state with S_z_tot = 0 (if filled_spots is even)
    initial_state = ["Emp" for n in 1:N]
    if filled_spots > 0
        positions = randperm(N)[1:filled_spots]
        for i in 1:filled_spots
            if isodd(i)
                initial_state[positions[i]] = "Up"
            else
                initial_state[positions[i]] = "Dn"
            end
        end
    end
    return initial_state
end

function calculate_filling(psi, sites) # calculates the tot filling
    N = length(sites)
    total_electrons = 0.0
    magz = expect(psi, "Ntot")
    total_electrons = sum(magz)
    filling = total_electrons / N
    return filling
end

function calculate_energy(t, J, N, neighbors, initial_state)

    sites = siteinds("tJ", N; conserve_qns=true)
    ampo = AutoMPO()

    for j in 1:N
        for neighbor in neighbors[j]
            if neighbor > j
                # Hopping term
                add!(ampo, -t, "Cdagup", j, "Cup", neighbor)
                add!(ampo, -t, "Cdagup", neighbor, "Cup", j)
                add!(ampo, -t, "Cdagdn", j, "Cdn", neighbor)
                add!(ampo, -t, "Cdagdn", neighbor, "Cdn", j)

                # Spin interaction term
                add!(ampo, 0.5 * J, "S+", j, "S-", neighbor)
                add!(ampo, 0.5 * J, "S-", j, "S+", neighbor)
                add!(ampo, J, "Sz", j, "Sz", neighbor)

                add!(ampo, -0.25 * J, "Ntot", j, "Ntot", neighbor)
            end
        end
    end

    H = MPO(ampo, sites)
    psi0 = randomMPS(sites, initial_state)
    nsweeps = 30 # n_sweeps
    maxdim = [10, 20, 40, 75, 100, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000] #\chi_max
    cutoff = [1E-12]
    noise = [1E-8, 0.0] # important or else DMRG is getting stuck
    energy, psi = dmrg(H,psi0; nsweeps, maxdim, cutoff, noise)

    # Calculate the local density
    local_density = expect(psi, "Ntot")
    #Calculate the local spin distr.
    local_spin = expect(psi, "Sz")

    return energy, psi, sites, local_density, local_spin
end

function calculate_correlation_functions(N, psi, sites, bonds)

    filling = calculate_filling(psi, sites)
    println("filling is:", filling)

    #Calculate the density density corr func
    local_density = expect(psi, "Ntot")
    density_density_corr_matrix = correlation_matrix(psi, "Ntot", "Ntot")
    for i in 1:N
        for j in 1:N
            density_density_corr_matrix[i, j] -= local_density[i] * local_density[j]
        end
    end

    # Calculate the spin-spin correlation function
    spinspin_corr_matrix = correlation_matrix(psi, "Sz", "Sz")

    # Compute all terms of the pairing operator Δ_i_dagger Δ_j with i and j as bond indices
    function precompute_ops(bonds, sites, len)
        half = 0.5
        minus_half = -0.5
        results = Dict{Tuple{Int, Int}, Any}()
        for k in 1:len
            for l in 1:len

                os = OpSum()
                i_1 = bonds[k][1]
                i_2 = bonds[k][2]
                j_1 = bonds[l][1]
                j_2 = bonds[l][2]
    
                os .+= (half, "Cdagdn", i_1, "Cdagup", i_2, "Cup", j_2, "Cdn", j_1)
                os .+= (minus_half, "Cdagdn", i_1, "Cdagup", i_2, "Cdn", j_2, "Cup", j_1)
                os .+= (minus_half, "Cdagup", i_1, "Cdagdn", i_2, "Cup", j_2, "Cdn", j_1)
                os .+= (half, "Cdagup", i_1, "Cdagdn", i_2, "Cdn", j_2, "Cup", j_1)

                results[(k, l)] = MPO(os, sites)
            end
        end
        return results
    end

    println("Starting to compute pair operators")
    len = length(bonds)
    precomputed_ops = precompute_ops(bonds, sites, len)
    println("Finished to compute pair operators")

    pairing_corr_matrix = zeros(Float64, len, len) # we want correlation matrix of Δ†_i with Δ_j

    function compute_expectation_value(Δ_sum, psi)
        return inner(psi', Δ_sum, psi)
    end

    for k in 1:len
        Δ_sums = [precomputed_ops[(k, l)] for l in 1:len]
        expectation_values = map(Δ_sum -> compute_expectation_value(Δ_sum, psi), Δ_sums)
        println("iteration $k of $len")
        pairing_corr_matrix[k, :] = expectation_values
    end

    return density_density_corr_matrix, spinspin_corr_matrix, pairing_corr_matrix
end

function main()
    t = 1
    stars = 5
    N = 8 + 7 * (stars - 1)
    #just delete stars and make N = integer for the chain
    
    J_values = 0.0:0.5:3.5
    n_values = [1/6]

    new_directory = "" # specify directory
    mkpath(new_directory)

    prev_neighbors, deleted_vertices = hexagon_strip_top_triangles_neighbors_connected_fully(stars)

    not_allowed_data = DataFrame(Site=1:(stars-1), SiteAllowedNotAllowed=deleted_vertices) # for python code, which was written earlier with different numeration
    CSV.write("$new_directory/not_allowed_values_for_sites.csv", not_allowed_data)

    neighbors = renumber(prev_neighbors, deleted_vertices)
    bonds = map_neighbors_to_bonds(neighbors)

    results = DataFrame(J=Float64[], n=Float64[], spin_gap=Float64[])

    for (i, J) in enumerate(J_values)
        for (j, n) in enumerate(n_values)

            filled_spots = Int(n * N)
            initial_state = create_random_initial_state(filled_spots, N)

            E_0, psi, sites, local_density, local_spin = calculate_energy(t, J, N, neighbors, initial_state)

            density_data = DataFrame(Site=1:N, LocalDensity=local_density)
            CSV.write("$new_directory/local_density_S0_$(J).csv", density_data)

            spin_data = DataFrame(Site=1:N, LocalSpin=local_spin)
            CSV.write("$new_directory/local_spin_S0_$(J).csv", spin_data)

            density_density_corr_matrix, spin_spin_corr_matrix, singlet_pairing_corr_matrix = calculate_correlation_functions(N, psi, sites, bonds)
            density_density_df = DataFrame(density_density_corr_matrix, :auto)
            CSV.write("$new_directory/density_density_corr_matrix_$(J).csv", density_density_df)
            spin_spin_df = DataFrame(spin_spin_corr_matrix, :auto)
            CSV.write("$new_directory/spin_spin_corr_matrix_$(J).csv", spin_spin_df)
            singlet_df = DataFrame(singlet_pairing_corr_matrix, :auto)
            CSV.write("$new_directory/singlet_pairing_corr_matrix_$(J).csv", singlet_df)

            #Calculate the eigenvalues of singlet pairing correlation function for QLRO
            eigenvalues = eigen(singlet_pairing_corr_matrix).values
            eigenvalue_data = DataFrame(Site=1:length(bonds), Eigenvalue=eigenvalues)
            CSV.write("$new_directory/eigenvalues_$(J).csv", eigenvalue_data)
            
            println("Finished calculating correlation func. Starting to calculate spingap")

            # Flipping one spin to calculate spin gap
            initial_state_flip = copy(initial_state)
            up_positions = findall(x -> x == "Up", initial_state_flip)
            dn_positions = findall(x -> x == "Dn", initial_state_flip)
            if length(dn_positions) > 0
                middle_dn_index = dn_positions[clamp(round(Int, length(dn_positions) / 2), 1, length(dn_positions))]
                initial_state_flip[middle_dn_index] = "Up"
            elseif length(up_positions) > 0
                middle_up_index = up_positions[clamp(round(Int, length(up_positions) / 2), 1, length(up_positions))]
                initial_state_flip[middle_up_index] = "Dn"
            end
            E_1, _, _, local_density, local_spin = calculate_energy(t, J, N, neighbors, initial_state_flip)

            density_data = DataFrame(Site=1:N, LocalDensity=local_density)
            CSV.write("$new_directory/local_density_S1_$(J).csv", density_data)

            spin_data = DataFrame(Site=1:N, LocalSpin=local_spin)
            CSV.write("$new_directory/local_spin_S1_$(J).csv", spin_data)

            spin_gap = E_1 - E_0
            push!(results, (J, n, spin_gap)) 

            CSV.write("$new_directory/spin_gap_and_energy.csv", results)
        end
    end
end
main()