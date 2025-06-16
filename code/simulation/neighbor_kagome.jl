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