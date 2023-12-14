# SWC 1
Dependency Management Demo: Software Component 1 (uses a shared module called **shared_module_a**)

## Preparation
You can resolve the SWC's dependencies by calling 
```sh
conan install . -r conanrepo
```

If you haven't configured conan yet, point it to the right repository by running "conan remote add". Here's an example for a conan repo in artifactory:
```sh
conan remote add conanrepo http://$host:$port/artifactory/api/conan/$reponame
```