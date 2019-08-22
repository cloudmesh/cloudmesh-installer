# FAQ

## (Only for class students) How to report an issue to us in piazza

Assume you have an issue with the cloudmesh install. 

a) It is not sufficient to send us a screenshot, send the ASCII text
b) It is not sufficinent to just send the ASCII text, but you must 

   1) mention the OS
   2) mention if you us pyenv or not
   3) mention if you run in a VM
   4) mention if you run cloudmesh in a container
   
The reason is that dependent on the answer we will ask you to simply restarts as 
this is the easiest.

## I used the curl install and get an issue

I get 

    ModuleNotFoundError: No module named 'cloudmesh.management'
    (ENV3) xxxx-MacBook-Pro:cm xxxx$ 
 
A dependency is not yet met. You may be able to fix it with 

    cd cloudmesh-cloud
    pip install -e .
    
In case it does not, please use the `cloudmesh-installer` approach wich is more
or less the same, but with much more advanced features.

## I followed the one line installer but it still did not work

There may be a dependency issue between older installs. You could try to uninstall 
all cloudmesh packages including the eggs you find. the egs you can find with 

    pip install cloudmesh-installer
    cloudmesh-installer local purge ~
    
Just delete them and do the install via the cloudmesh-installer instead. However
the curl install should work after you purge the old versions. If not, let us know.

See `Install on a bare machine`


## Install on a bare machine 

We assume that may or may not have pyenv installed. We prefer you to use pyenv

Place your cloudmesh.yaml file in ~/.cloudmesh/cloudmesh.yaml
    
    mkdir cm
    cd cm
    pip install cloudmesh-installer
    cloudmesh-installer git clone cms
    cloudmesh-installer install cms -e
    
Now open a new terminal (the old one where you executed the commands you can close

    cms help 
    
These command should work. If not, please contact us, you can reach Gregor or a TA 
for this almost immediatly, starting Tjursday afternoon. send a private post to piazza 
and somone will be with you shortly.

After this dependent on which project you do, storage, or cloud you need to do the following.


    cloudmesh-installer git clone cloud
    cloudmesh-installer install cloud -e

or    

    cloudmesh-installer git clone storage
    cloudmesh-installer install storage -e


The cloud install will take a while we saww everything from 1-5 minutes. However
if you have a real old machine it may take longer. For example, I had yesterday
a call with a student that had a super old Mac book air, which results in very
long compile times. IN this case we almost recommend that you use a VM elsewhere
and do the development remotely. On older Linux based systems we saw install
times of 1 minute. On a 1 year old mac that runs a virus checker it takes 5
minutes. On a Mac without virus checker switched off during the install it takes
about a minute.

Open a new terminal and check

    
    cms help 
    cms version

you should see that it is working. If not contact us with a private post in
piazza considering our post about how to report the error
    
## Try to recover as you for some reason can not start fresh

a) make sure to delete all old versions of cloudmesh. Pip freze may help to discover if you have one installed

    pip freeze | fgrep cloudmesh
    
   delete or uninstall them
   
b) In case you need help with us the following options exist


## Uninstall a pyenv

We assume the pyenv is called ENV3 as recommended in the handbook

    pip install cloudmesh-installer
    cloudmesh-installer pyenv purge ENV3 --force
    
Then follwo the steps in Uninstall old cloudmesh instalations

## Uninstall old cloudmesh instalations

Start a new terminal and create an empty directory

    mkdir cm
    cd cm
    pip install cloudmesh-installer
    cloudmesh-installer local purge ~
    
If you see some hits, you can say    
    
    cloudmesh-installer local purge ~ --force

Do 

    pip freeze | fgrep cloudmesh
    
If you see anything, make sure to locate that install and uninstall them or they
will conflict with your other installs. Typicially repeated pip uninstall of the
found library will do.

Now that it is uninstalled, you can follow the steps as outlined in 

the FAQ `Install on a bare machine`

## I am working on virtual machines cloud package

Follow the advice above if you need to repair. If you have a vanilla system you can say

    mkdir cm
    cd cm
    pip install cloudmesh-installer
    cloudmesh-installer git clone cloud
    cloudmesh-installer install cloud -e
    
start a new terminal if you installed it in pyenv

   cms help vm
## I am working on virtual machines storage package

Follow the advice above if you need to repair. If you have a vanilla system you can say

    mkdir cm
    cd cm
    pip install cloudmesh-installer
    cloudmesh-installer git clone storage
    cloudmesh-installer install storage -e
    
start a new terminal if you installed it in pyenv

    cms help vm

## I used anaconda

In case you used anaconda, please contact the TA Bo who is using anaconda and
can give instructions. 


## Something is different and I can not figure it out

Get in contact with Gregor, he is not available Thursday and Friday morning, but
otherwise he is there if not in other meetings. We ran the installation on
multiple students and TA's computers and if something does not work, please let
us know. so we can help.

## TheAzure cloud modules take a long tiem to install

Yes it takes up to five minutes, On older machines may be longer. 





