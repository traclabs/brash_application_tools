cmake_minimum_required(VERSION 3.5)

project(tracarm_description)

find_package(ament_cmake REQUIRED)


set(ament_cmake_copyright_FOUND TRUE)

install(DIRECTORY launch urdf meshes
  DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()