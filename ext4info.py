#!/usr/bin/env python3

import fire
import struct
import uuid

BLOCKSIZE = 1024
EXT4MAGIC = 0xEF53

#struct size_of defines
LE16 = '<H'
LE32 = '<L'
U8 = 'B'

class Ext4Superblock:
    def __init__(self, filename):
        self.filename = filename
        self.superblock = None
        try:
            with open(filename, 'rb') as filesystem:
                filesystem.seek(BLOCKSIZE) # seek past boot block
                self.superblock = filesystem.read(BLOCKSIZE)  # read in presumed superblock
        except EnvironmentError as e:
            print(e)
            raise
        
        # Test if magic number matches Ext4 specification 0xEF53
        if(self.get_magic(raw=True) != EXT4MAGIC):
            raise ValueError('{} not a valid ext4 filesystem.'.format(self.filename))

    def get_magic(self, raw=False):
        magic = struct.unpack_from(LE16, self.superblock, 0x38)[0] 

        if raw:
            return magic
        else:
            return hex(magic)

    def get_total_inode_count(self):
        return struct.unpack_from(LE32, self.superblock, 0x00)[0]

    def get_total_block_count(self):
        return struct.unpack_from(LE32, self.superblock, 0x04)[0]

    def get_reserved_block_count(self):
        return struct.unpack_from(LE32, self.superblock, 0x08)[0]

    def get_free_blocks_count(self):
        return struct.unpack_from(LE32, self.superblock, 0x0C)[0]

    def get_free_inodes_count(self):
        return struct.unpack_from(LE32, self.superblock, 0x10)[0]

    def get_first_data_block(self):
        return struct.unpack_from(LE32, self.superblock, 0x14)[0]

    def get_s_log_block_size(self):
        return struct.unpack_from(LE32, self.superblock, 0x18)[0]

    def get_block_size(self):
        return 1024 << self.get_s_log_block_size() 

    def get_s_log_cluster_size(self):
        # conditional on checking bigalloc feature supported. le32 at 0x1c
        raise NotImplementedError('get_s_log_cluster_size not yet implemented')

    def get_cluster_size(self):
        raise NotImplementedError('get_cluster_size not yet implemented')

    def get_blocks_per_group(self):
        return struct.unpack_from(LE32, self.superblock, 0x20)[0]

    def get_clusters_per_group(self):
         # conditional on checking bigalloc feature supported. le32 at 0x24
        raise NotImplementedError('get_clusters_per_group not yet implemented')

    def get_inodes_per_group(self):
        return struct.unpack_from(LE32, self.superblock, 0x28)[0]

    def get_time_last_mounted(self, raw=False):
        mtime = struct.unpack_from(LE32, self.superblock, 0x2C)[0]

    def get_volume_uuid(self, raw=False):
        uuid_raw = self.superblock[0x68:0x78]

        if raw:
            return uuid_raw
        else:
            return uuid.UUID(bytes=uuid_raw)

    def dump_raw_superblock(self):
        return self.superblock


def dumpe2fs_info(filename, raw=False):
    sb = Ext4Superblock(filename)
    print('Magic Number: {}'.format(sb.get_magic()))

    print('Total Inodes: {}'.format(sb.get_total_inode_count()))
    
    print('Total Blocks: {}'.format(sb.get_total_block_count()))

    print('Reserved Blocks: {}'.format(sb.get_reserved_block_count()))

    print('Free Inodes: {}'.format(sb.get_free_inodes_count()))

    print('Free Blocks: {}'.format(sb.get_free_blocks_count()))

    print('First Data Block: {}'.format(sb.get_first_data_block()))

    print('Block size: {}'.format(sb.get_block_size()))

    print('Volume UUID: {}'.format(sb.get_volume_uuid()))


if __name__ == "__main__":
    fire.Fire(dumpe2fs_info)
