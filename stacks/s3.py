from aws_cdk import (
    aws_ssm as ssm,
    aws_s3 as s3,
    core
)


class S3Stack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id)

        account_id = core.Aws.ACCOUNT_ID
        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        # pipeline artifacts bucket
        artifacts_bucket = s3.Bucket(self, 'artifact-bucket',
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
        core.CfnOutput(self, 's3-build-artifacts-export',
                       value=artifacts_bucket.bucket_name,
                       export_name='build-artifacts-bucket')





