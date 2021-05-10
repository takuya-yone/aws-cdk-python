from aws_cdk import (
    core as cdk,
    aws_ec2
)

prefix :str = 'PREFIX'
ec2_keyname :str = 'KEYNAME'

class BaseFormationStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        base_vpc = aws_ec2.Vpc(
            self,
            id='{}-vpc'.format(prefix),
            cidr='10.0.0.0/16',
            nat_gateways=0, # NatGatewayを作成しない指定
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name='{}-public-subnet'.format(prefix),
                    subnet_type=aws_ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                aws_ec2.SubnetConfiguration(
                    name='{}-private-subnet'.format(prefix),
                    subnet_type=aws_ec2.SubnetType.ISOLATED,
                    cidr_mask=24
                )
            ],
        )

        my_ec2_security_group = aws_ec2.SecurityGroup(
            self,
            id='{}-ec2-sg'.format(prefix),
            vpc=base_vpc,
            allow_all_outbound=True,
            security_group_name='{}-ec2-sg'.format(prefix),
        )

        my_ec2_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.ipv4('0.0.0.0/0'),
            connection=aws_ec2.Port.tcp(22),
            description='allow ssh access'
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
            id='{}-ec2-public-instance'.format(prefix),
            instance_type=aws_ec2.InstanceType.of(
                aws_ec2.InstanceClass.BURSTABLE2,
                aws_ec2.InstanceSize.MICRO
            ),
            machine_image=amzn_linux,
            vpc=base_vpc,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PUBLIC
            ),
            instance_name='{}-ec2-public-instance'.format(prefix),
            security_group=my_ec2_security_group,
            key_name = ec2_keyname
        )

        my_ec2_instance = aws_ec2.Instance(
            self,
            id='{}-ec2-private-instance'.format(prefix),
            instance_type=aws_ec2.InstanceType.of(
                aws_ec2.InstanceClass.BURSTABLE2,
                aws_ec2.InstanceSize.MICRO
            ),
            machine_image=amzn_linux,
            vpc=base_vpc,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.ISOLATED
            ),
            instance_name='{}-ec2-private-instance'.format(prefix),
            security_group=my_ec2_security_group,
            key_name = ec2_keyname
        )

        # for i in range(1,4):
        #     aws_ec2.Instance(
        #         self,
        #         id='{}-ec2-private-instance-seq{}'.format(prefix,str(i)),
        #         instance_type=aws_ec2.InstanceType.of(
        #             aws_ec2.InstanceClass.BURSTABLE2,
        #             aws_ec2.InstanceSize.MICRO
        #         ),
        #         machine_image=amzn_linux,
        #         vpc=base_vpc,
        #         vpc_subnets=aws_ec2.SubnetSelection(
        #             subnet_type=aws_ec2.SubnetType.ISOLATED
        #         ),
        #         instance_name='{}-ec2-private-instance-seq{}'.format(prefix,str(i)),
        #         security_group=my_ec2_security_group,
        #         key_name = ec2_keyname
        #     )
