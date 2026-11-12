# Map theorem source packet

Read-only excerpts from STeP-Formalization, commit `df815bafacf94dbae369b7cb57b44d6ad93a0950`.

Source: [STeP/Operators/Map.lean:16](https://github.com/lanmogu98/STeP-Formalization/blob/df815bafacf94dbae369b7cb57b44d6ad93a0950/STeP/Operators/Map.lean#L16-L18)

```lean
/-- Unary STeP `Map`: apply a payload function to every data token. -/
def map (f : α → β) (s : Stream α) : Stream β :=
  Stream.mapData f s
```

Source: [STeP/Operators/Map.lean:95](https://github.com/lanmogu98/STeP-Formalization/blob/df815bafacf94dbae369b7cb57b44d6ad93a0950/STeP/Operators/Map.lean#L95-L98)

```lean
theorem map_commutes (f : α → β) (rank : Nat) (ts : List (Tensor α)) :
    WellRankedSeq rank ts →
      decode rank (map f (encode rank ts)) = ts.map (Tensor.map f) := by
  simpa [map] using decode_stream_mapData_encode f rank ts
```

Source: [STeP/Foundation/Tensor.lean:148](https://github.com/lanmogu98/STeP-Formalization/blob/df815bafacf94dbae369b7cb57b44d6ad93a0950/STeP/Foundation/Tensor.lean#L148-L150)

```lean
/-- Every tensor in a stream-level sequence satisfies the declared rank discipline. -/
def WellRankedSeq (rank : Nat) (ts : List (Tensor α)) : Prop :=
  ts.all (Tensor.wellRanked rank) = true
```
