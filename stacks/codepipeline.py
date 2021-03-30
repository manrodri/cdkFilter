from aws_cdk import (
    aws_codepipeline as cp,
    aws_codepipeline_actions as cp_actions,
    aws_codebuild as cb,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_s3 as s3,
    core

)

class CodePipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, artifactbucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        artifact_bucket = s3.Bucket.from_bucket_name(
            self, 'artifactbucket', artifactbucket)



        github_token = core.SecretValue.secrets_manager(
            secret_id=f'{env_name}/github-token', json_field='github-token'
        )

        pipeline = cp.Pipeline(self, 'test-pipeline',
                               pipeline_name=f'{env_name}-{prj_name}',
                               artifact_bucket=artifact_bucket,
                               restart_execution_on_update=False,
                               )

        source_output = cp.Artifact(artifact_name='source')

        pipeline.add_stage(stage_name='Source',
                           actions=[
                               cp_actions.GitHubSourceAction(
                                   oauth_token=github_token,
                                   output=source_output,
                                   repo='testLZFilter',
                                   branch='master',
                                   owner='manrodri',
                                   action_name='GitHubSource'
                               )
                           ])

        deploy_bucket = s3.Bucket(self, 'deploy-bucket',
                                  access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                  encryption=s3.BucketEncryption.S3_MANAGED,
                                  block_public_access=s3.BlockPublicAccess(
                                      block_public_acls=True,
                                      block_public_policy=True,
                                      ignore_public_acls=True,
                                      restrict_public_buckets=True
                                  ),
                                  removal_policy=core.RemovalPolicy.DESTROY
                                  )



        deploy_action = cp_actions.S3DeployAction(
            action_name="S3Deploy",
            bucket=deploy_bucket,
            input=source_output,
            extract=False,
            object_key='aws-landing-zone-configuration.zip'
        )
        pipeline.add_stage(
            stage_name='Deploy',
            actions=[
                deploy_action
            ]
        )

        # ssm params
        ssm.StringParameter(
            self, 'bucket-name', parameter_name=f'/{env_name}/{prj_name}/deploy-bucket-name', string_value=deploy_bucket.bucket_name)
        ssm.StringParameter(
            self, 'pipeline-arn', parameter_name=f'/{env_name}/{prj_name}/pipeline-name', string_value=pipeline.pipeline_arn)










