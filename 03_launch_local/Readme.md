# Launching a local instance of cBioportal using Docker

### How to start a local instance of cBioportal on your computer

The following is a set of instructions that help you spin up a local instance of cBioportal. 
You can use this to test uploading you study folder and visualize it before submitting to the institutional or public instance.

1. Download the latest version of Docker from here: [https://www.docker.com/#/install_the_platform]

2. Once installed open the application and login

3. Open a terminal window and go to the directory where you would want to setup the local instance of cBioportal.
   ```
   cd /path/to/the/directory/where/you/want/to/setup/cBioportal
   ```

5. Download the cbioportal github repository by copying this command into terminal.

```
git clone https://github.com/cBioPortal/cbioportal-docker-compose.git
```

6. Now change your directory  to the root directory of the downloaded folder
```
cd cbioportal-docker-compose
```
7. Then download all necessary files (seed data, example config and example study from datahub) with the init script.
```
./init.sh

```

This can take sometime, wait for the necessary downloads to complete.

8. Then run
```
docker compose up

```

This setup starts four containers: 
- a MySQL database for cBioPortal data
- the cBioPortal Java web app (which serves the frontend and REST API)
- a session service Java web app (with a REST API that stores session/user data in MongoDB)
- and the MongoDB database itself.

The first run imports the seed database and applies migrations. 
Logs from each container are shown, and if there are no critical errors, cBioPortal will be accessible at http://localhost:8080 from your favorite browser (Chrome, Safari etc.), though no studies will be displayed initially.

_Note: Let the terminal keep running in the background_

After testing this for the first time you can also start cBioportal locally without logging everything to the terminal by doing this:
```
docker compose up -d

```

You can check logs for each container manually (if needed):
```
docker logs -f cbioportal_container
```

And you can list all the containers running on your system:

```
docker ps -a
```

### Uploading a test study to view on your locally running instance 

You can now import an example study into your locally running instance. 
```
docker compose run cbioportal metaImport.py -u http://cbioportal:8080 -s study/lgg_ucsf_2014/ -o
```

This can take some time as well...

Then you must restart your cBioportal instance 
```
docker compose restart cbioportal
```
Once your study is done downloading you must refresh the browser to be able to see the study on the local run of cBioportal

All public studies can be downloaded from https://www.cbioportal.org/datasets, or https://github.com/cBioPortal/datahub/.
You can add any of them to the ./study folder (located in the root directory where you have downloaded cBioportal in) and import them. 

There's also a script (./study/init.sh) to download multiple studies. 
You can set DATAHUB_STUDIES to any public study id (e.g. lgg_ucsf_2014) and run ./init.sh.

### Uploading your study to view on the local instance 

In order to use this local instance to see how your study will look you can copy your prepared files into the ./study folder.



### cBioportal documentation

Detailed instructions on how to deploy a local instance of cBioportal with Docker(https://docs.cbioportal.org/deployment/docker/#deploy-with-docker)
