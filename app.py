from aws_cdk import core
from stacks.codepipeline import CodePipelineStack
from stacks.s3 import S3Stack

app = core.App()

s3_stack = S3Stack(app, 's3buckets', env={'region': 'eu-west-1'})
cp_backend = CodePipelineStack(app, 'cp-backend',
                               artifactbucket=core.Fn.import_value('build-artifacts-bucket'),
                               env={'region': 'eu-west-1'})

app.synth()
