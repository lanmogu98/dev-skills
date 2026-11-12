# Illustrative tiled-kernel control flow

This is synthetic algorithm input for diagram validation, not a STeP implementation or a proved theorem.

Inputs are a contiguous array x, length n ≥ 0, and a tile capacity B > 0. An output array of length n is available. The kernel applies the same elementwise transform to each valid element.

1. If n = 0, return the empty output without loading or storing data.
2. Otherwise select the next tile, visiting tiles in increasing offset order.
3. If the tile is full and meets the vector path's alignment condition, load it using the vector path. Otherwise use a safe fallback that loads only valid elements. These alternatives are mutually exclusive, not parallel tasks.
4. Both paths rejoin at the same elementwise transform. Store only valid elements of this tile.
5. If more tiles remain, return to next-tile selection. Otherwise return the completed output.

The fallback handles both a partial final tile and an unaligned full tile. There is no reduction, asynchronous prefetch, or inter-thread barrier in the supplied algorithm. Do not add these to make the diagram appear more sophisticated.
