from aws_cdk import (
    core,
    aws_ec2
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
# from aws_cdk import core

ec2_keyname = "aiueo"

class AwsCdkPythonStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        my_vpc = aws_ec2.Vpc(
            self,
            id="my-vpc",
            cidr="192.168.0.0/16",
            nat_gateways=0, # NatGatewayを作成しない指定
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name="my-public-subnet",
                    subnet_type=aws_ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                aws_ec2.SubnetConfiguration(
                    name="my-private-subnet",
                    subnet_type=aws_ec2.SubnetType.ISOLATED,
                    cidr_mask=24
                )
            ]
        )

        my_ec2_security_group = aws_ec2.SecurityGroup(
            self,
            id="my-ec2-sg",
            vpc=my_vpc,
            allow_all_outbound=True,
            security_group_name="my-ec2-sg"
        )

        my_ec2_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.ipv4("0.0.0.0/0"),
            connection=aws_ec2.Port.tcp(22),
            description="allow ssh access"
        )

        amzn_linux = aws_ec2.MachineImage.latest_amazon_linux(
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX,
            edition=aws_ec2.AmazonLinuxEdition.STANDARD,
            virtualization=aws_ec2.AmazonLinuxVirt.HVM,
            storage=aws_ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            cpu_type=aws_ec2.AmazonLinuxCpuType.X86_64
        )

        my_ec2_instance = aws_ec2.Instance(
            self,
            id="my-ec2-instance",
            instance_type=aws_ec2.InstanceType.of(
                aws_ec2.InstanceClass.BURSTABLE2,
                aws_ec2.InstanceSize.MICRO
            ),
            machine_image=amzn_linux,
            vpc=my_vpc,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PUBLIC
            ),
            instance_name="my-ec2-instance",
            security_group=my_ec2_security_group,
            key_name = ec2_keyname
        )

        for i in range(1, 4):
            aws_ec2.Instance(
                self,
                id="my-ec2-instance-seq" + str(i),
                instance_type=aws_ec2.InstanceType.of(
                    aws_ec2.InstanceClass.BURSTABLE2,
                    aws_ec2.InstanceSize.MICRO
                ),
                machine_image=amzn_linux,
                vpc=my_vpc,
                vpc_subnets=aws_ec2.SubnetSelection(
                    subnet_type=aws_ec2.SubnetType.ISOLATED
                ),
                instance_name="my-ec2-instance-seq" + str(i),
                security_group=my_ec2_security_group,
                key_name = ec2_keyname
        )