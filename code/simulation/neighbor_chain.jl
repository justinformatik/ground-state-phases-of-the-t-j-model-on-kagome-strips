function one_d_chain(num_vertices)
    neighbors = Dict{Int, Vector{Int}}()

    for v in 1:num_vertices
        neighbors_list = []
        if v > 1
            push!(neighbors_list, v - 1)
        end
        if v < num_vertices
            push!(neighbors_list, v + 1)
        end
        neighbors[v] = neighbors_list
    end

    return neighbors
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