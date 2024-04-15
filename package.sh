#! /bin/bash
filename=nujnus_`date +"%Y_%m_%d_%H_%M_%S"`.tar.gz
tar zcvf ../${filename}  .git
echo 打包完成:${filename}