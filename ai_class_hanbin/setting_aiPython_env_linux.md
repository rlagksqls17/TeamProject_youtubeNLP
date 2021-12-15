## 설치 버전

<Ubuntu LTS 20.04>

nvidia driver 버전 : 460.91.03

CUDA 버전 : 11.2_460.32.03

cuDNN 버전 : 8.1

동작 가능한 tensorflow 버전 : 2.6.0

동작 가능한 torch 버전 : 1.10.0

python : 3.6 ~ 3.9

---

## ubuntu 버전 확인

![image-20211127170926484](C:\Users\joo\AppData\Roaming\Typora\typora-user-images\image-20211127170926484.png)

---

## GPU 설치 확인  

```
sudo lspci -v | less  
```

![image-20211127163423316](C:\Users\joo\AppData\Roaming\Typora\typora-user-images\image-20211127163423316.png)

---

## nvidia driver 버전 확인

```
nvidia-smi 
```

![image-20211127164041600](C:\Users\joo\AppData\Roaming\Typora\typora-user-images\image-20211127164041600.png)

또한 이 nvidia driver가 돌아가고 있는지 확인하는 방법은 없을까?  

- nbidia-smi는 실제 nvidia 모듈이 로드된 경우에만 작동한다. 

---

## 설치된 패키지 확인

```
sudo apt --installed list
```

![image-20211127165956825](C:\Users\joo\AppData\Roaming\Typora\typora-user-images\image-20211127165956825.png)

- 설치된 드라이버 자체가 없음을 확인함



## 그래픽 카드 확인 위해 nvidia-smi 설치가 필요하다고 생각함

``` 
sudo apt remove ubuntu-drivers-common (설치 후 삭제 함, 명확한 버전 표기 X)
추천은 nvidia-drivers-470임  
```

nvidia-utils-460 설치하여 nvidia-smi 실행했지만 잡힌 건 없었음 (근데 애초에 드라이버가 설치가 안되어 있으니 당연한 걸지도?) 

드라이버 설치 후에 nvidia-smi로 gpu 돌아가는게 있는지 확인해야 할듯 

설치 - nvidiasmi - reboot - nvidiasmi - 성공  

![image-20211127225020902](C:\Users\joo\AppData\Roaming\Typora\typora-user-images\image-20211127225020902.png)

이제 cuda를 설치해야 하는데, cuda의 버전은 11.2의 460.32.03, 하지만 nvidia 버전은 460.91.03 이라서 mistmatch 문제가 나면 어쩌지 하는 걱정이 됬음  

근데 다른 블로그에서는 이 문제는 별로 신경쓰지 않는 듯  

https://sanglee325.github.io/environment/install-CUDA-11-2/#11-%EC%97%90%EB%9F%AC%EA%B0%80-%EB%B0%9C%EC%83%9D%ED%95%9C-%EA%B2%BD%EC%9A%B0-building-kernel-modules  

---

## cuda  설치

<파일 동작 완료>

![image-20211127230752994](C:\Users\joo\AppData\Roaming\Typora\typora-user-images\image-20211127230752994.png)

<path 등록>

```
$ vim ~/.bashrc

# 입력
export PATH=/usr/local/cuda-11.2/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.2/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.2/extras/CUPTI/lib64:$LD_LIBRARY_PATH

$ source ~/.bashrc
```

<설치 확인>

```
nvcc -V
```

![image-20211127231437393](C:\Users\joo\AppData\Roaming\Typora\typora-user-images\image-20211127231437393.png)

---

## cudnn 설치  

```
$ tar -zxvf cudnn-11.2-linux-x64-v8.1.1.33.tgz

$ cd cuda

$ cp include/cudnn* /usr/local/cuda-11.2/include/

$ cp lib64/libcudnn* /usr/local/cuda-11.2/lib64/

$ chmod a+r /usr/local/cuda-11.2/lib64/libcudnn*
```

```
$ cat /usr/local/cuda-11.2/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
```

cudnn 설치 확인 완료

![image-20211127233745850](C:\Users\joo\AppData\Roaming\Typora\typora-user-images\image-20211127233745850.png)

## 도움이 많이 되었던 블로그

http://blog.ju-ing.com/posts/offline-nvidia-gpu-setting/
