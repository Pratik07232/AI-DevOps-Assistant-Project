from flask import Flask, request, jsonify

app = Flask(__name__)
TROUBLESHOOTING_DATA = {

    "crashloopbackoff": {
        "problem": "Kubernetes Pod is repeatedly restarting.",
        "causes": [
            "Application is crashing",
            "Incorrect environment variables",
            "Incorrect startup command"
        ],
        "commands": [
            "kubectl logs <pod-name>",
            "kubectl describe pod <pod-name>"
        ],
        "solution": "Check the Pod logs first, then inspect the Pod configuration."
    },

    "imagepullbackoff": {
        "problem": "Kubernetes cannot pull the container image.",
        "causes": [
            "Incorrect image name",
            "Image does not exist",
            "Private registry authentication problem"
        ],
        "commands": [
            "kubectl describe pod <pod-name>",
            "docker pull <image-name>"
        ],
        "solution": "Verify the image name, tag, registry and credentials."
    },

    "docker permission denied": {
        "problem": "Docker permission denied while accessing the Docker daemon.",
        "causes": [
            "User does not have permission to access Docker",
            "Docker daemon is not running",
            "Incorrect Docker socket permissions"
        ],
        "commands": [
            "docker ps",
            "docker info",
            "docker logs <container-name>"
        ],
        "solution": "Check that Docker is running and verify the user's permission to access the Docker daemon."
    },

    "kubernetes connection refused": {
        "problem": "Unable to connect to the Kubernetes API server.",
        "causes": [
            "Kubernetes cluster is not running",
            "kubectl is using the wrong context",
            "Kubernetes API server is unavailable"
        ],
        "commands": [
            "kubectl cluster-info",
            "kubectl config current-context",
            "kubectl get nodes"
        ],
        "solution": "Check that the Kubernetes cluster is running and verify the current kubectl context."
    },

    "port already in use": {
        "problem": "The requested port is already being used.",
        "causes": [
            "Another container is using the port",
            "Another application is using the port"
        ],
        "commands": [
            "docker ps",
            "docker stop <container-id>"
        ],
        "solution": "Find the process using the port and stop it or use another port."
    },

    "container exited": {
        "problem": "The Docker container stopped after starting.",
        "causes": [
            "Application crashed",
            "Incorrect CMD or ENTRYPOINT",
            "Missing dependency"
        ],
        "commands": [
            "docker ps -a",
            "docker logs <container-id>"
        ],
        "solution": "Check the container logs to identify why the application stopped."
    }
}


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "AI DevOps Troubleshooting Service"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data or "error" not in data:
        return jsonify({
            "error": "Please provide an error message."
        }), 400

    user_error = data["error"].lower().strip()

    # Check top-level troubleshooting keywords
    for keyword, result in TROUBLESHOOTING_DATA.items():

        if keyword in user_error:

            # Nested troubleshooting data
            if isinstance(result, dict) and "problem" not in result:

                for sub_keyword, sub_result in result.items():

                    if sub_keyword in user_error:
                        return jsonify({
                            "matched": True,
                            "query": data["error"],
                            **sub_result
                        })

            else:
                return jsonify({
                    "matched": True,
                    "query": data["error"],
                    **result
                })

    # Check nested keywords independently
    for category, result in TROUBLESHOOTING_DATA.items():

        if isinstance(result, dict):

            for sub_keyword, sub_result in result.items():

                if sub_keyword in user_error:

                    return jsonify({
                        "matched": True,
                        "query": data["error"],
                        **sub_result
                    })

    return jsonify({
        "matched": False,
        "query": data["error"],
        "problem": "The error was not found in the current knowledge base.",
        "causes": [
            "Unknown or unsupported error"
        ],
        "commands": [
            "Check application logs",
            "Check container logs",
            "Check Kubernetes events"
        ],
        "solution": "Collect the exact error message and investigate the relevant service logs."
    })