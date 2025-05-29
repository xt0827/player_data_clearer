from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'clear_player_data',
    'version': '1.0.0',
    'name': 'ClearPlayerData',
    'description': '清除指定UUID的玩家数据',
    'author': 'Xcuk',
    'link': 'https://github.com/xt0827/clear-player-data',
    'dependencies': {
        'mcdreforged': '>=2.0.0',
    }
}


# 配置类
class Config(Serializable):
    world_dir: str = 'world'  # 世界文件夹名称
    playerdata_dir: str = 'playerdata'  # 玩家数据文件夹名称


# 全局变量
config: Config = None


def delete_player_data(server: ServerInterface, uuid: str) -> bool:
    """删除指定UUID的玩家数据文件"""
    import os

    # 构建文件路径
    playerdata_path = os.path.join(
        server.get_mcdr_config()['working_directory'],
        config.world_dir,
        config.playerdata_dir,
        f'{uuid}.dat'
    )

    # 检查文件是否存在
    if not os.path.isfile(playerdata_path):
        server.logger.info(f"玩家数据文件不存在: {playerdata_path}")
        return False

    # 尝试删除文件
    try:
        os.remove(playerdata_path)
        server.logger.info(f"成功删除玩家数据文件: {playerdata_path}")
        return True
    except Exception as e:
        server.logger.error(f"删除玩家数据文件失败: {e}")
        return False


def on_load(server: ServerInterface, old_module):
    """插件加载时调用"""
    global config

    # 加载配置
    config = server.load_config_simple(target_class=Config)

    # 注册命令
    server.register_command(
        Literal('!!cpd')
        .then(Text('uuid').runs(lambda src, ctx: handle_command(src, ctx['uuid'])))
    )

    # 注册帮助信息
    server.register_help_message('!!cpd <uuid>', '清除指定UUID的玩家数据')


def handle_command(source: CommandSource, uuid: str):
    """处理命令请求"""
    # 检查权限
    if source.has_permission(4):  # OP权限
        source.get_server().logger.info(f"收到清除玩家数据请求: UUID={uuid}")
        if delete_player_data(source.get_server(), uuid):
            source.reply(f"§a成功清除UUID为 {uuid} 的玩家数据")
        else:
            source.reply(f"§c清除玩家数据失败，请检查控制台日志获取详细信息")
    else:
        source.reply("§c你没有权限执行此命令")