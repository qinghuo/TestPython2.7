#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt,sys

def usage():
    print("Usage:%s [-a|-o|-c] [--help|--output] args...." %(sys.argv[0]))

if __name__=='__main__':
    try:
        shortargs = 'f:t'
        longargs = ['directory-prefix=', 'format', '--f_long=']
        opts,args= getopt.getopt( sys.argv[1:], shortargs, longargs)
        print('****************opts********************')
        print('opts=',opts)
        print('****************args********************')
        print('args=',args)

        for opt,arg in opts:
            if opt in ('-h','--help'):
                usage()
                sys.exit(1)
            elif opt in ('--f_long'):
                print('--f_long=',opt)
            else:
                print('%s====> %s' %(opt,arg))
    except getopt.GetoptError:
        print('getopt error!')
        usage()
        sys.exit(1)