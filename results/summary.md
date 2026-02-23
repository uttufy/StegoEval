# StegoEval Benchmark Summary

## Average Performance per Algorithm & Attack

| algorithm   | attack_category   | attack_name   |    psnr |     ssim |      ber |   ncc_secret |
|:------------|:------------------|:--------------|--------:|---------:|---------:|-------------:|
| example_lsb | compression       | jpeg          | 73.6288 | 0.999867 | 0.485429 |    0.0128939 |
| example_lsb | compression       | webp          | 73.6288 | 0.999867 | 0.480457 |    0.0158435 |
| example_lsb | filtering         | gaussian_blur | 73.6288 | 0.999867 | 0.476426 |    0.0176076 |
| example_lsb | filtering         | median        | 73.6288 | 0.999867 | 0.452097 |    0.0216633 |
| example_lsb | geometric         | cropping      | 73.6288 | 0.999867 | 0.472715 |    0.0168469 |
| example_lsb | geometric         | rotation      | 73.6288 | 0.999867 | 0.459286 |    0         |
| example_lsb | geometric         | scaling       | 73.6288 | 0.999867 | 0.477662 |    0.0173575 |
| example_lsb | noise             | gaussian      | 73.6288 | 0.999867 | 0.499221 |    0.0140065 |
| example_lsb | noise             | salt_pepper   | 73.6288 | 0.999867 | 0.207868 |    0.349224  |
| example_lsb | noise             | speckle       | 73.6288 | 0.999867 | 0.501498 |    0.0152068 |
| example_lsb | none              | clean         | 73.6288 | 0.999867 | 0        |    1         |