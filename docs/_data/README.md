Data read by code cells at build time; not rendered as pages.

- `jetstream2-nodes.csv` — worker sizes. `disk_fs_gib` is what `df` reports on a worker;
  `overhead_gib` is OS + Docker + harness; `footprint_factor` is on-disk / compressed size
  of a pulled image (measured 2026-08-22: dynare 3.41x, rocker 3.69x, julia ~4.4x; 3.5 is the middle).
- `container-images.csv` — representative images for the size table. `compressed_gib` is
  looked up from Docker Hub when blank; GHCR images have no public size API, so their
  figure is entered by hand (`measured` = date read from the registry manifest).
