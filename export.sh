#!/bin/bash

## CURRENT DIR
cd "`dirname \"$0\"`"

PWD="`pwd`"

## CONFIG
PROJECT_PATH="Unity-iPhone.xcodeproj"
SCHEME_NAME="UnityFramework"
CONFIGURATION_NAME="Release"
DESTINATION_NAME="generic/platform=iOS"
EXPORT_ROOT_DIR="$PWD/export"
FRAMEWORK_PATH="$EXPORT_ROOT_DIR/$SCHEME_NAME.framework"
DSYM_PATH="$EXPORT_ROOT_DIR/$SCHEME_NAME.framework.dSYM"
XC_FRAMEWORK_PATH="$EXPORT_ROOT_DIR/$SCHEME_NAME.xcframework"

echo "当前路径：$PWD"

CommitShortId="$(git rev-parse --short HEAD)"
echo "commit short id：$CommitShortId"
mkdir ~/Documents/Work/CommitShortId

## CLEAN DIR
echo "[##### Start cleaning dir ... #####]"
if [ -d "$EXPORT_ROOT_DIR" ]; then
    rm -rf "$EXPORT_ROOT_DIR"
fi
mkdir "$EXPORT_ROOT_DIR"
echo "[##### Finish cleaning dir. #####]"

## CLEAN BUILD
echo ""
echo "[##### Start cleaning build ... #####]"
xcodebuild clean -project "$PROJECT_PATH" -scheme "$SCHEME_NAME" -destination "$DESTINATION_NAME"
echo "[##### Finish cleaning build. #####]"

## BUILD
echo ""
echo "[##### Start building ... #####]"
xcodebuild build CONFIGURATION_BUILD_DIR="$EXPORT_ROOT_DIR" -project "$PROJECT_PATH" -scheme "$SCHEME_NAME" -configuration "$CONFIGURATION_NAME" -destination "$DESTINATION_NAME"

if [ $? != 0 ]; then
echo "[===== Build failed, exit now!!! =====]"
exit 1
fi

echo "[##### Finish building. #####]"

## Export xcframework
echo ""
echo "[##### Start exporting ... #####]"
xcodebuild -create-xcframework -framework "$FRAMEWORK_PATH" -debug-symbols "$DSYM_PATH" -output "$XC_FRAMEWORK_PATH"
echo "[##### Finish exporting. #####]"

mv $XC_FRAMEWORK_PATH ~/Documents/Work/$CommitShortId/$SCHEME_NAME.xcframework
if [ -d "$EXPORT_ROOT_DIR" ]; then
    rm -rf "$EXPORT_ROOT_DIR"
fi

echo ""
echo "[##### Done! #####]"
