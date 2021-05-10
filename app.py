#!/usr/bin/env python3
import os


# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core as cdk
# from aws_cdk.core import App, Stack, Tags

from aws_cdk_python.aws_cdk_python_stack import BaseFormationStack


app = cdk.App()

BaseFormationStack = BaseFormationStack(app, 'STACKNAME')
# BaseFormationStack.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY)
cdk.Tags.of(BaseFormationStack).add('Name', 'TAGVALUE')

app.synth()
