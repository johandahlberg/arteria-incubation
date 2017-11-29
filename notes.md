To get everything up and running I ran:

```
cp /opt/stackstorm/packs/arteria/default.config.yaml /opt/stackstorm/configs/
st2 run packs.setup_virtualenv packs=arteria
st2ctl reload --register-configs

# Restart appears to be necessary to sensor to pickup config
st2ctl restart st2sensorcontainer

st2 rule enable arteria.when_runfolder_is_ready_start_test
```

Running the bcl2fastq service:

```
curl -X POST --data '{}' bcl2fastq-service/api/1.0/start/150605_M00485_0183_000000000-ABGT6_testbio14
```
