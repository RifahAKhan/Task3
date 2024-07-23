load("@rules_python//python:defs.bzl", "py_binary")
load("@rules_pkg//pkg:zip.bzl", "pkg_zip")

py_binary(
  name = "smartModel",
  srcs = ["smartModel.py"],
  
)

pkg_zip(
    name = "PackagesmartModel", 
    srcs = ["//:smartModel"],
    out = "smartModelDeployment.zip",
    )

