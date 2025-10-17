import subprocess, os, sys


IMAGE = os.environ.get('IMAGE_NAME', 'demo/model:staging')


# build image
subprocess.run(['docker', 'build', '-t', IMAGE, '.'], check=True)
# run container (stop previous if exists)
# Note: in CI runner, docker daemon may not be available. Use this locally or in runners with docker.
try:
    subprocess.run(['docker', 'rm', '-f', 'ml_model_staging'], check=False)
except Exception:
    pass
subprocess.run(['docker', 'run', '-d', '--name', 'ml_model_staging', '-p', '8080:8080', IMAGE], check=True)
print('Deployed image to local docker as ml_model_staging')