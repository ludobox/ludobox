# Config

All config options are in `config.yml` file.

```yaml
# config file for your Ludobox

ludobox_name : "My LudoBox"
port: 8080 # the port to serve the interface (default to 8080)

# The source of your games
web_server_url : null

# Directory to store all downloaded data -- default to ./data
# data_dir : /home/$USER/ludobox/data

# enable/disable creation of new games on the box
upload_allowed : true

```

### `ludobox_name` The name of your LudoBox

This name will be used to identify your box in the network.

* It is shown on your box's homepage.
* ex. ```ludobox_name : "My LudoBox"```

### `port` Web Port Number

The web port to serve the interface

* default : 8080
* ex. ```port : 8080```

### `web_server_url`  Remote server URL

The remote server is the source where you can download your games.

* The URL should point to another Ludobox instance.
* When set to `null`, the download will be disabled and the `Download` button will be hidden from the navbar
* default : [http://box.ludobox.net](http://box.ludobox.net)
* ex. ```web_server_url : http://box.ludobox.net```

### `data_dir` Data Directory

The directory to store all downloaded data

* Default :  ./data
* ex. ```data_dir : /home/$USER/ludobox/data```

### `upload_allowed` Upload Allowed

Simple boolean switch to enable/disable creation of new games on the box

* When upload is disable, the `add game` feature will be hidden from nav bar.
* ex. ```upload_allowed : true```
