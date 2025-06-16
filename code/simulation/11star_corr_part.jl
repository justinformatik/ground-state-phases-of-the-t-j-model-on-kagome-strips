function calculate_correlation_functions(N, psi, sites, bonds)

    # Calculate filling
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

    function precompute_ops(bonds, sites, k, l)
        half = 0.5
        minus_half = -0.5
        os = OpSum()
        i_1 = bonds[k][1]
        i_2 = bonds[k][2]
        j_1 = bonds[l][1]
        j_2 = bonds[l][2]
        os .+= (half, "Cdagdn", i_1, "Cdagup", i_2, "Cup", j_2, "Cdn", j_1)
        os .+= (minus_half, "Cdagdn", i_1, "Cdagup", i_2, "Cdn", j_2, "Cup", j_1)
        os .+= (minus_half, "Cdagup", i_1, "Cdagdn", i_2, "Cup", j_2, "Cdn", j_1)
        os .+= (half, "Cdagup", i_1, "Cdagdn", i_2, "Cdn", j_2, "Cup", j_1)
        result = MPO(os, sites)
        return result
    end

    println("Starting to compute pair corr func")
    len = length(bonds)
    pairing_corr_matrix = zeros(Float64, len, len) # we want correlation matrix of Δ†_i with Δ_j

    function compute_expectation_value(Δ_sum, psi)
        return inner(psi', Δ_sum, psi)
    end

    from_chain_bonds = [100, 74, 71, 106, 107, 89, 87, 22, 20, 83, 81, 126, 31, 33, 54, 15, 12, 29, 26, 92, 35] #not all entries are needed for <Δ†_i Δ_j> over |i - j|

    for k in from_chain_bonds
        for l in from_chain_bonds
            Δ = precompute_ops(bonds, sites, k, l)
            pairing_corr_matrix[k, l] = compute_expectation_value(Δ, psi)
            print("done")
        end
    end
    return density_density_corr_matrix, spinspin_corr_matrix, pairing_corr_matrix
end