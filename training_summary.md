# Training Summary Report

**Generated:** 2026-01-04 23:47:46

## Training Configuration

```
population_size: 100
num_generations: 500
mutation_probability: 0.2
mutation_gaussian_sigma: 0.15
crossover_probability: 0.7
max_workers: 16
frame_delay: 0.016666666666666666
```

## Overall Summary

- **Total Generations:** 278
- **Training Duration:** 0:45:54.195070
- **All-Time Best Fitness:** 7027.92
- **Best Generation:** 263
- **Final Best Fitness:** 4922.85
- **Final Average Fitness:** 1514.38
- **Avg Improvement (Early->Late):** 463.42
- **Stagnation:** 15 generations since improvement

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 11.72
- **Avg Steps Survived:** 406
- **Avg Accuracy:** 73.1%
- **Max Kills (Any Agent Ever):** 70
- **Max Steps (Any Agent Ever):** 1500

## Learning Progress

**Comparing First 27 vs Last 27 Generations:**

| Metric       | Early  | Late   | Change |
| ------------ | ------ | ------ | ------ |
| Best Fitness | 3495.5 | 4067.0 | +16.3% |
| Avg Fitness  | 888.7  | 1213.0 | +36.5% |

**Verdict:** Moderate learning - some improvement but room for more training.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 755.06
- Average Range (Best-Min): 3868.82
- Diversity Change: +6.0%
- **Status:** Population has moderate diversity (healthy)

## Behavioral Trends

| Period | Avg Kills | Avg Steps | Avg Accuracy | Max Kills |
| ------ | --------- | --------- | ------------ | --------- |
| Q1     | 10.95     | 393       | 65.1%        | 69        |
| Q2     | 10.54     | 379       | 68.5%        | 63        |
| Q3     | 12.28     | 415       | 74.1%        | 66        |
| Q4     | 11.75     | 400       | 73.2%        | 70        |

## Stagnation Analysis

- **Current Stagnation:** 15 generations
- **Average Stagnation Period:** 54.4 generations
- **Longest Stagnation:** 227 generations
- **Number of Stagnation Periods:** 5

## Recent Generations (Last 30)

| Gen | Best | Avg  | StdDev | Kills | Steps | Acc% | Stag |
| --- | ---- | ---- | ------ | ----- | ----- | ---- | ---- |
| 249 | 2712 | 1029 | 304    | 10.3  | 404   | 81   | 214  |
| 250 | 3915 | 850  | 722    | 8.5   | 340   | 73   | 215  |
| 251 | 599  | 334  | 117    | 3.4   | 185   | 41   | 216  |
| 252 | 299  | 222  | 58     | 2.2   | 141   | 50   | 217  |
| 253 | 2510 | 175  | 366    | 1.8   | 175   | 26   | 218  |
| 254 | 4615 | 1276 | 697    | 12.7  | 404   | 79   | 219  |
| 255 | 4922 | 948  | 994    | 9.5   | 315   | 64   | 220  |
| 256 | 4519 | 445  | 707    | 4.5   | 208   | 47   | 221  |
| 257 | 4020 | 777  | 600    | 7.7   | 322   | 74   | 222  |
| 258 | 4823 | 2338 | 772    | 23.3  | 662   | 90   | 223  |
| 259 | 3308 | 1667 | 706    | 16.6  | 539   | 87   | 224  |
| 260 | 4924 | 1257 | 650    | 12.5  | 399   | 82   | 225  |
| 261 | 4319 | 232  | 494    | 2.3   | 172   | 28   | 226  |
| 262 | 4223 | 1884 | 847    | 18.7  | 563   | 89   | 227  |
| 263 | 7028 | 2226 | 1344   | 22.2  | 591   | 82   | 0    |
| 264 | 4723 | 1811 | 737    | 18.0  | 553   | 88   | 1    |
| 265 | 6926 | 2395 | 1075   | 23.9  | 653   | 87   | 2    |
| 266 | 3019 | 1191 | 860    | 11.8  | 422   | 79   | 3    |
| 267 | 3420 | 1170 | 504    | 11.6  | 442   | 90   | 4    |
| 268 | 1402 | 981  | 199    | 9.8   | 362   | 80   | 5    |
| 269 | 1911 | 884  | 541    | 8.8   | 355   | 74   | 6    |
| 270 | 4318 | 2082 | 888    | 20.7  | 645   | 87   | 7    |
| 271 | 4020 | 1331 | 902    | 13.3  | 455   | 84   | 8    |
| 272 | 5421 | 1314 | 963    | 13.1  | 435   | 78   | 9    |
| 273 | 4632 | 757  | 840    | 7.5   | 272   | 62   | 10   |
| 274 | 4823 | 647  | 995    | 6.5   | 247   | 48   | 11   |
| 275 | 5825 | 1992 | 839    | 19.9  | 600   | 82   | 12   |
| 276 | 1002 | 325  | 240    | 3.3   | 229   | 52   | 13   |
| 277 | 3935 | 911  | 675    | 9.1   | 357   | 78   | 14   |
| 278 | 4923 | 1514 | 804    | 15.1  | 467   | 85   | 15   |

## Top 10 Best Generations

| Rank | Gen | Best | Avg  | Kills | Steps | Accuracy |
| ---- | --- | ---- | ---- | ----- | ----- | -------- |
| 1    | 263 | 7028 | 2226 | 70    | 1500  | 97.9%    |
| 2    | 265 | 6926 | 2395 | 69    | 1500  | 95.7%    |
| 3    | 35  | 6922 | 2177 | 69    | 1500  | 95.7%    |
| 4    | 171 | 6624 | 681  | 66    | 1500  | 93.5%    |
| 5    | 186 | 6425 | 1803 | 64    | 1500  | 100.0%   |
| 6    | 24  | 6332 | 2305 | 63    | 1500  | 96.8%    |
| 7    | 230 | 6332 | 1080 | 63    | 1500  | 95.7%    |
| 8    | 145 | 6326 | 1828 | 63    | 1457  | 98.9%    |
| 9    | 125 | 6326 | 2031 | 63    | 1500  | 96.8%    |
| 10   | 179 | 6324 | 2321 | 63    | 1404  | 96.6%    |

## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
| ------ | -------- | -------- | ------- | ----------- |
| Q1     | 3656.5   | 1098.7   | 166.8   |             |
| Q2     | 3304.0   | 1057.1   | 238.9   | -352.5      |
| Q3     | 3767.0   | 1232.4   | 306.4   | +463.1      |
| Q4     | 3862.5   | 1178.6   | 283.9   | +95.4       |

## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

    6624 |                                  *
    6182 |                                     *
    5741 |               *             *                **
    5299 |       **       *          *
    4858 |         * *
    4416 |  ***     * *           * *      *  *       *      *
    3974 |     *       *                                   *  * *
    3533 | *            *             *  *         *      *
    3091 |                                      *
    2650 |                 * *     *                           *
    2208 |       o        o    *  o    o         *
    1766 |*          o           *       o     o      o  o
    1325 |     o  o o  o o   o      ooo   *o              o     o
     883 | o oo    o  o       *o        * o  *o  o o*  *   o   o *
     442 |      *           *      o    o   o   o *    oo   *o
       0 |o o   o       o  oo o *o           o    o o*      o o  o
         --------------------------------------------------------
         Gen 1                                         Gen 278
```
