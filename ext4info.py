#!/usr/bin/env python3

import fire
import struct
import uuid
import time

BLOCKSIZE = 1024
EXT4MAGIC = 0xEF53

SB_ERROR_POLICY = {
    1: 'Continue',
    2: 'Remount read-only',
    3: 'Panic at the Disco',
}

FS_CREATOR = {
    0: 'Linux',
    1: 'Hurd',
    2: 'Masix',
    3: 'FreeBSD',
    4: 'Lites',

}

SB_REV = {
    0: 'original',
    1: 'V2',
}

STATE_MASKS = {
    0x0001: 'cleanly_unmounted',
    0x0002: 'errors_detected',
    0x0004: 'orphans_being_recovered'
}

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

    def __format_timestamp(self, timestamp):
        if timestamp > 0:
            return time.ctime(timestamp)
        else:
            return 'n/a'

    def get_time_last_mounted(self, raw=False):
        mtime = struct.unpack_from(LE32, self.superblock, 0x2C)[0]
        
        if raw:
            return mtime 
        else:
            return self.__format_timestamp(mtime)

    def get_time_last_write(self, raw=False):
        wtime = struct.unpack_from(LE32, self.superblock, 0x30)[0]
        
        if raw:
            return wtime 
        else:
            return self.__format_timestamp(wtime)

    def get_mount_count(self):
        return struct.unpack_from(LE32, self.superblock, 0x34)[0]

    def __bitmask_flags(self, field, masks):
        flags_present = []
        for mask, description in masks.items():
            if field & mask:
                flags_present.append(description)
        
        return ' '.join(flags_present)

    def get_superblock_state(self, raw=False):
        state = struct.unpack_from(LE16, self.superblock, 0x3A)[0]
        
        if raw:
            return state
        else:
            return self.__bitmask_flags(state, STATE_MASKS)

    def get_error_policy(self, raw=False):
        policy_raw = struct.unpack_from(LE16, self.superblock, 0x3C)[0]

        if raw:
            return policy_raw
        else:
            return SB_ERROR_POLICY[policy_raw]

    def get_creator_os(self, raw=False):
        creator_raw = struct.unpack_from(LE16, self.superblock, 0x3E)[0]

        if raw:
            return creator_raw
        else:
            return FS_CREATOR[creator_raw]

    def get_volume_uuid(self, raw=False):
        uuid_raw = self.superblock[0x68:0x78]

        if raw:
            return uuid_raw
        else:
            return uuid.UUID(bytes=uuid_raw)

    def get_journal_uuid(self, raw=False):
        uuid_raw = self.superblock[0xD0:0xE0]

        if raw:
            return uuid_raw
        else:
            return uuid.UUID(bytes=uuid_raw)

    def get_volume_label(self, raw=False):
        label_raw = self.superblock[0x78:0x88]

        if raw:
            return label_raw
        else:
            return "".join(chr(c) for c in label_raw)

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

    print('Blocks per group: {}'.format(sb.get_blocks_per_group()))

    print('Inodes per group: {}'.format(sb.get_inodes_per_group()))

    print('Time last mounted: {}'.format(sb.get_time_last_mounted()))
    
    print('Time last write: {}'.format(sb.get_time_last_write()))

    print('State Flags: {}'.format(sb.get_superblock_state()))

    print('Volume Label: {}'.format(sb.get_volume_label()))

    print('Volume UUID: {}'.format(sb.get_volume_uuid()))


if __name__ == "__main__":
    fire.Fire(dumpe2fs_info)
