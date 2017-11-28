To get everything up and running I ran:

```
# TODO Probably also need to copy the default config in place?
cp /opt/stackstorm/packs/arteria/default.config.yaml /opt/stackstorm/configs/
st2 run packs.setup_virtualenv packs=arteria
st2ctl reload --register-configs

# Restart appears to be necessary to sensor to pickup config
st2ctl restart st2sensorcontainer

st2 rule enable arteria.when_runfolder_is_ready_start_test
```
