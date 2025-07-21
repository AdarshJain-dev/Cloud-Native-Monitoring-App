import boto3
from kubernetes import client, config

config.load_kube_config()

api_client = client.ApiClient()

#Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "my-flask-app"}),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="654654540441.dkr.ecr.us-east-1.amazonaws.com/my-cloud-native-repository:latest",
                        ports=[client.V1ContainerPort(container_port=5000)],
                    )
                ]
            )
        )
    )
)

# Create the deployment
apps_v1 = client.AppsV1Api(api_client)
apps_v1.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)],
    )
)

# Create the service
core_v1 = client.CoreV1Api(api_client)
core_v1.create_namespaced_service(
    namespace="default",
    body=service
)
