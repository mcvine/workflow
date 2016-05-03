# copy share files
file(COPY ./
  DESTINATION ${EXPORT_SHARE}/workflow/
  PATTERN "CMakeLists.txt" EXCLUDE
  PATTERN "*~" EXCLUDE
  )


# tests
set(BUILD_TESTS_PATH ${TESTS_DIR}/workflow)
# copy tests to build
file(COPY tests/ DESTINATION ${BUILD_TESTS_PATH})
# add python tests
PYUNITTEST_ADD_TESTS_IN_DIR( ${BUILD_TESTS_PATH} workflow)
