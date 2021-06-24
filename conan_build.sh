git submodule update --init --recursive
conan create . --build missing
# you should paste the output of the previous command below:
conan install diligent-engine/2.5@ -g deploy
