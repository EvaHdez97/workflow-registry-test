# Software Catalog

This is a repository to store the description of the software to be used in computational HPC workflows using the eFlows4HPC methodology. 

## Repository structure

Software descriptions have to be included inside this repository according to the following structure

```
software-catalog
  |- packages
  |    |- software_1
  |    |    |- package.py		Installation description following the Spack package format
  |    |    |- invocation.json          Description of the software invocation
  |    |       ...
  |    |- software_2    
  |          ....
  |- cfg				Spack configuration used by the Image Creation Service	
  |    
  |- repo.yaml				Spack description of for this repository  

```  

## Including new software

To include new  software in the repository, create a fork of the repository including the description of the new software including at least the spack package description and invocation description. Then, create a create pull request with the branch of the newly added software. This pull request will be reviewed an added to merge to the repository.

