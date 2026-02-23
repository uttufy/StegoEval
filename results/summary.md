# StegoEval Benchmark Summary

## Average Performance per Algorithm & Attack

| algorithm   | attack_category   | attack_name   |    psnr |   ssim |      ber |   ncc_secret |
|:------------|:------------------|:--------------|--------:|-------:|---------:|-------------:|
| example_lsb | compression       | jpeg          | 90.1085 |      1 | 0.507273 |   0.0127063  |
| example_lsb | compression       | webp          | 90.1085 |      1 | 0.517828 |   0.0322623  |
| example_lsb | filtering         | gaussian_blur | 90.1085 |      1 | 0.508463 |   0.0297455  |
| example_lsb | filtering         | median        | 90.1085 |      1 | 0.418305 |   0.0506781  |
| example_lsb | geometric         | cropping      | 90.1085 |      1 | 0.47151  |   0.0186212  |
| example_lsb | geometric         | rotation      | 90.1085 |      1 | 0.329545 |   0          |
| example_lsb | geometric         | scaling       | 90.1085 |      1 | 0.494211 |   0.0447411  |
| example_lsb | noise             | gaussian      | 90.1085 |      1 | 0.545127 |   0.0281941  |
| example_lsb | noise             | salt_pepper   | 90.1085 |      1 | 0.108779 |   0.628152   |
| example_lsb | noise             | speckle       | 90.1085 |      1 | 0.558502 |   0.00982722 |
| example_lsb | none              | clean         | 90.1085 |      1 | 0        |   1          |