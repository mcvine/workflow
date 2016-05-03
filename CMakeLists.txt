install(
  DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
  DESTINATION share/mcvine/workflow/
  USE_SOURCE_PERMISSIONS
  PATTERN "CMakeLists.txt" EXCLUDE
  PATTERN "*~" EXCLUDE
  )


# tests
set(BUILD_TESTS_PATH ${TESTS_DIR}/workflow)
# copy tests to build
file(COPY tests/ DESTINATION ${BUILD_TESTS_PATH})
# add python tests
PYUNITTEST_ADD_TESTS_IN_DIR( ${BUILD_TESTS_PATH} workflow)
