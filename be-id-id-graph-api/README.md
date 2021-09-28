# ID-Graph API
This project hosts the code and build scripts for the API that returns necessary 
information for two divisions to share data.

## Input
The ID_Graph API bases on the CRM ID-Graph. The ID-Graph is a table that holds 
a column for every company that participates in the B-ID project. A row 
corresponds to a unique customer that is known in any of these companies. The 
entries of the lines are the customer CRM IDs of the corresponding company. If there are multiple CRM IDs within one row it means that the customer was found
in more than one CRM dataset.

Besides these company columns there is another column called `cell_id`. This
column assigns groups of customers into groups (~cells). This data is used for
highly sensitive data where a sharing on person level is not allowed.
In the following you can see an exemplary ID-Graph table:

company_1 | company_2 | company_3 | cell_id 
--- | --- | --- | --- 
123 |  |  | A1
234| BCD | XYZ | B2
652| DEF |  | B2
523|  | XYZ | C3
545| MNO | UZA | D4

## API objective
This API is called when sharing information for two companies is necessary. It 
distinguishes between sharing on person level and sharing on cell level. It will
return the CRM IDs for the customers that both companies have in common and
enriches them with a (random) sharing ID that will be used for the effective sharing. In the sharing process itself company_1 will not see the CRM IDs of company_2 and
vice versa.

### Sharing on person level

Exaple for a share between company_2 and company_3 on person level:

company_2 | sharing_id 
--- | --- 
BCD | 684615679
MNO | 321568132

company_3 | sharing_id 
--- | --- 
XYZ | 684615679
UZA | 321568132

### Sharing on cell level

If company_1 and company_2 will chare data on cell level the tables would be the
following:

company_1 | sharing_id 
--- | --- 
234| 354931234
652| 354931234
545| 651684644

company_2 | sharing_id 
--- | --- 
BCD | 354931234
DEF | 354931234
MNO | 651684644


## API functionality
The API has two routs that specify if the sharing will be done on a person level 
or on a microcell level (`share_person` and `share_cell`).

In both cases the API takes two parameters (`company_1` and `company_2`) that specify the two companies that 
want to share data.

exemplary calls on person level:
localhost:8000/share_person/?company_1=com_1&company_2=com_2

exemplary calls on cell level:
localhost:8000/share_cell/?company_1=com_1&company_2=com_2



## Build Related
### Dockerfile
The [Dockerfile](./Dockerfile) is the file used for building the containers. All
dependencies are stored in`requirements.txt` besides the code.

### Pipeline
The definitions for the GitHub Action Pipeline are in the `.github`-folder. It
automatically builds the image and pushes it to the coresponding Azure Container
Registry. Besides that it also forces the Azure Web App to update its image.


## Local Testing

If you want to run the API locally you have either to grant yourself access to 
the corresponding storage account and key vault and add its URLs in the code or 
use the given test data from test_data.py by importing it via 
`from test_data import df_id_graph` and outcommenting the code that corresponds
to the data reading from Azure.
