# Figure reconstruction

## Recover the chart semantics

Identify:

- chart geometry and statistical transformation;
- source ranges or plotted-data columns;
- x, y, series, group, and panel mappings;
- aggregation level and category order;
- uncertainty intervals, smoothers, or fitted lines;
- scale transformations, axis limits, units, breaks, and reference lines;
- legends, annotations, labels, and source notes;
- intended physical dimensions and output format.

An Excel chart may depend on helper ranges that contain the real analytical transformation. Trace those ranges rather than copying only the final series values.

## Create a plotting dataset

Save or construct the exact data passed to the plotting library. Include stable series and panel identifiers, explicit ordering fields, and lower or upper bounds where applicable. This plotting dataset is the primary object for equivalence testing.

## Reproduce meaning before decoration

Match observations, aggregation, scales, and geometry before colors or typography. Do not force pixel identity across different rendering engines. Preserve meaningful encodings and approximate purely decorative details when exact replication would require brittle or proprietary behavior.

Produce one rendered format. Follow an explicit user request first, then the project's publication convention; otherwise use PNG. Do not automatically create PDF, SVG, or a separate preview. The plotting code and plotting data provide the reproducible, Git-trackable source even when the PNG itself is not meaningfully diffable.
