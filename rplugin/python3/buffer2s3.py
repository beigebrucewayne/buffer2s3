import neovim
import boto3


@neovim.plugin
class Buffer2s3:
    """Neovim Integration for AWS S3

    The reason for this plugin was mainly pedagogical. Does
    it have some real functionality? Yeah. Should you actually use it?
    Ehh...maybe.

    Examples:

    :S3Buckets ---> list out all buckets in S3
    :S3BucketFiles 'bucket_name' ---> list out all files in S3 buckets
    """
    def __init__(self, nvim):
        self._nvim = nvim
        self._cur_buf = self._nvim.current.buffer
        self._cur_buf_path = self._cur_buf.name
        self._s3 = boto3.client('s3')
        self._s3r = boto3.resource('s3')
        self._buckets = self._s3.list_buckets()
        self._bucket_names = [bucket['Name'] for bucket in self._buckets['Buckets']]

    #TODO: Implement Buffer2S3() method

    @neovim.command('S3Buckets')
    def s3buckets(self):
        """List out all buckets within S3"""
        all_buckets = ' '.join('{}'.format(i) for i in self._bucket_names)
        self.echo(f'[--S3 Buckets--]: {all_buckets}')

    @neovim.command('S3BucketFiles', nargs='*')
    def s3bucketfiles(self, args):
        """List out all files within an S3 Bucket"""
        bucket = args
        content = self._s3.list_objects(Bucket=bucket)['Contents']
        files = [key['Key'] for key in content]
        all_files = ' '.join('{}'.format(i) for i in files)
        self.echo(f'[--Bucket Files--]: {all_files}')

    def echo(self, message):
        """Write out S3 information to Neovim"""
        self._nvim.command_output('echo "{}"'.format(message))
