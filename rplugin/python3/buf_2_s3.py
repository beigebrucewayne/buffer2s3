import neovim
import boto3


@neovim.plugin
class B2S3:

    def __init__(self, nvim):
        self._nvim = nvim
        self.cur_buf = self._nvim.current.buffer
        self.cur_buf_path = self.cur_buf.name
        self._s3 = boto3.client('s3')
        self._s3r = boto3.resource('s3')
        self._buckets = self._s3.list_buckets()
        self.buckets = [bucket['Name'] for bucket in self._buckets['Buckets']]

    #  @neovim.command('Buffer2S3')
    #  def buffer2s3(self):
        #  a, *b, cur_buf_name = self.cur_buf_path.split('/')
        #  buf_to_write = write_buffer(cur_buf_name)

    @neovim.command('S3Buckets')
    def s3buckets(self):
        string_of_buckets = ' '.join('{}'.format(i) for i in self.buckets)
        self.echo(f'[S3 BUCKETS]: {string_of_buckets}')

    @neovim.command('S3BucketFiles')
    def s3bucketfiles(self, bucket):
        content = self._s3.list_objects(Bucket=bucket)['Contents']
        string_of_files = ' '.join('{}'.format(i) for i in content)
        self.echo(f'[FILEs]: {string_of_files}')

    def echo(self, message):
        self._nvim.command_output('echo "{}"'.format(message))


    #  def write_buffer(self, filename):
        #  #  vim_file = 'vim_{}'.format(filename)
        #  #  with open(vim_file, 'w') as file:
            #  #  file.write(''.join('{}\n'.format(i) for i in cur_))
        #  with tempfile.TemporaryDirectory() as tmpdirname:
            #  file_path = '{}/{}'.format(tmpdirname, filename)
            #  with open(file_path, 'w') as file:
                #  file.write(''.join('{}\n'.format(i)
                                   #  for i in self.cur_buf.range(1, len(self.cur_buf))))
