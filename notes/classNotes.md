DataMining Class Notes
=======================

## Lec4 Data Warehousing

### OLAP vs OLTP
- historical data
- simple updates vs complex queries



| OLTP | OLAP |
|:-----|:-----|
| simple updates | complex queries |
| more simultaneous queries | lesser simultaneous queries |
| | slower to update |


### Data Warehouse types

- Enterprise
	- often expensive
	- like for entire UC Berkeley
- Data Mart
	- smaller
	- limited in scope
- Virtual
	- OLAP built on top of OLTP database
- Cloud
	- Google BigQuery
	- Amazon Redshift
	

### Data Cubes / Lattice of cuboids
These are generally used for data with dimensions already discovered. The __dimensionality of data needs to be _rigid_. __

#### Cubes > Star > Snowflake > Constellation
It can easily get complicated.

Cube idea is visualize in head how to build queries. 


#### Tasks / Queries

- Rollup
	- going up. summarizing dimensions into fewer
- Drill-Down
	- Get details within a particular dimension.
- Slice
	- Select a particular value in a dimension
- Dice
	- Consider a subset of a values in a dimension
- Pivot
	- Swap/Rotate dimensions.