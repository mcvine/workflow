cmake_minimum_required (VERSION 2.6)
project (workflow)

set(VERSION "0.1.0a4")
set(AUTHOR "Jiao Lin")
set(AUTHOR_EMAILE "jiao.lin@gmail.com")
set(VENDOR "MCViNE")
set(SUMMARY "mcvine.workflow python subpackage")
set(LICENSE "BSD")
set(RPM_APP_GROUP "Development/Tools")
set(GITHUB_URL "https://github.com/mcvine/workflow")
set (HOMEPAGE ${GITHUB_URL})

# dependencies
set (CONDA_PKGING_BUILD_DEPS "mcvine")
set (CONDA_PKGING_RUN_DEPS "mcvine")

# variables
set (PARENT_PATH "mcvine")
set (PARENT_PY_PKG "mcvine")
set (PARENT_GITHUB_URL "https://github.com/mcvine/mcvine")
set (PARENT_VERSION "1.3")
set (PARENT_RELEASE "1")
set (PKG_NAME "${PARENT_PY_PKG}.${PROJECT_NAME}")


# get cmake_utils -- need it for testing
IF(EXISTS "cmake_utils/")
  execute_process(
    COMMAND git pull
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/cmake_utils
    )
ELSE(EXISTS "cmake_utils/")
  execute_process(
    COMMAND git clone https://github.com/danse-inelastic/cmake_utils
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
ENDIF(EXISTS "cmake_utils/")
set(CMAKE_MODULE_PATH ${PROJECT_BINARY_DIR}/cmake_utils)
# use utils
# include(System) # system info
include(Dirs)   # directory structure
include(TestUtils)
# message("lib: $ENV{LD_LIBRARY_PATH}; python: $ENV{PYTHONPATH}")


# needs python
find_package ( PythonLibs REQUIRED )
find_package ( PythonInterp REQUIRED )
# python installation path
set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(INSTALL_PY_PATH "${INSTALL_LIB_DIR}/python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}/site-packages")


# copy all python source over to build directory
file(COPY workflow DESTINATION "modules/mcvine/")
# and install
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/modules/
  DESTINATION ${INSTALL_PY_PATH}
  )


# copy share files
file(COPY share/
  DESTINATION ${EXPORT_SHARE}/mcvine/workflow/
  PATTERN "CMakeLists.txt" EXCLUDE
  PATTERN "*~" EXCLUDE
  PATTERN ".git*" EXCLUDE
  )
# install share
install(DIRECTORY ${EXPORT_SHARE}/ DESTINATION share/ USE_SOURCE_PERMISSIONS)


# tests
enable_testing()
set(BUILD_TESTS_PATH ${TESTS_DIR}/workflow)
# copy tests to build
file(COPY tests/ DESTINATION ${BUILD_TESTS_PATH})
# add python tests
PYUNITTEST_ADD_TESTS_IN_DIR( ${BUILD_TESTS_PATH} workflow)
