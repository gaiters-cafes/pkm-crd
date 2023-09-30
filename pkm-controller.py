import os
import time
from kubernetes import client as api_instance, config, watch

# Load Kubernetes configuration
config.load_kube_config()

# Define the Pokemon resource group and version
group = "datacenter.com"
version = "v1"
plural = "pokemons"

# Define the function to create a pod
def create_pokemon_pod(pokemon_name):
    pod_name = f"pokemon-{pokemon_name}"
    container_name = "pokemon-colorscripts"
    container_image = "bosssuperod/gaiters-pokemon:1.0"
    container_command = ['sh', '-c', f'pokemon-colorscripts -n {pokemon_name}']

    pod_manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": pod_name},
        "spec": {
            "containers": [
                {
                    "name": container_name,
                    "image": container_image,
                    "command": container_command
                }
            ]
        },
    }

    api_instance.CoreV1Api().create_namespaced_pod(namespace="default", body=pod_manifest)

# Define the main controller loop
def controller_loop():
    resource_version = ""
    while True:
        print("Watching for Pokemon CR changes...")
        stream = watch.Watch().stream(
            api_instance.CustomObjectsApi().list_namespaced_custom_object,  # Corrected here
            namespace="default",
            group=group,
            version=version,
            plural=plural,
            resource_version=resource_version,
        )

        for event in stream:
            obj = event["object"]
            resource_version = obj["metadata"]["resourceVersion"]
            pokemon_name = obj["metadata"]["name"]
            event_type = event["type"]

            if event_type == "ADDED":
                print(f"Pokemon {pokemon_name} created. Creating a pod...")
                create_pokemon_pod(pokemon_name)
            elif event_type == "DELETED":
                print(f"Pokemon {pokemon_name} deleted. Deleting its pod...")
                pod_name = f"pokemon-{pokemon_name}"
                api_instance.CoreV1Api().delete_namespaced_pod(name=pod_name, namespace="default")  # Corrected here

# Run the controller
if __name__ == "__main__":
    try:
        controller_loop()
    except KeyboardInterrupt:
        pass
