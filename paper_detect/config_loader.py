#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置加载工具

自动从配置文件加载API密钥和其他设置
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional


class Config:
    """配置管理器"""
    
    def __init__(self):
        self._config = {}
        self._loaded = False
    
    def load(self, config_file: str = None) -> bool:
        """
        加载配置文件
        
        参数:
            config_file: 配置文件路径（可选）
        
        返回:
            是否成功加载
        """
        if self._loaded:
            return True
        
        # 查找配置文件
        if config_file:
            config_paths = [config_file]
        else:
            # 默认查找位置
            project_root = Path(__file__).parent.parent
            config_paths = [
                project_root / 'config_api.py',
                Path.cwd() / 'config_api.py',
                Path.home() / '.paper_detect_config.py'
            ]
        
        # 尝试加载配置
        for config_path in config_paths:
            if Path(config_path).exists():
                try:
                    # 动态导入配置文件
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("config", config_path)
                    config_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(config_module)
                    
                    # 读取配置项
                    self._config = {
                        key: getattr(config_module, key)
                        for key in dir(config_module)
                        if not key.startswith('_') and key.isupper()
                    }
                    
                    self._loaded = True
                    print(f"✓ 已加载配置文件: {config_path}")
                    return True
                    
                except Exception as e:
                    print(f"警告: 加载配置文件失败 ({config_path}): {e}")
                    continue
        
        print("警告: 未找到配置文件 (config_api.py)")
        return False
    
    def get(self, key: str, default=None):
        """获取配置项"""
        if not self._loaded:
            self.load()
        return self._config.get(key, default)
    
    @property
    def api_key(self) -> Optional[str]:
        """获取API密钥"""
        key = self.get('SILICONFLOW_API_KEY')
        if key and key != 'your_api_key_here':
            return key
        return None
    
    @property
    def api_base(self) -> str:
        """获取API基础URL"""
        return self.get('SILICONFLOW_API_BASE', 'https://api.siliconflow.cn/v1')
    
    @property
    def model(self) -> str:
        """获取模型名称"""
        return self.get('SILICONFLOW_MODEL', 'Qwen/Qwen3-VL-32B-Instruct')
    
    @property
    def enable_content_check(self) -> bool:
        """是否启用图片内容检测"""
        return self.get('ENABLE_FIGURE_CONTENT_CHECK', False)
    
    @property
    def save_images(self) -> bool:
        """是否保存提取的图片"""
        return self.get('SAVE_EXTRACTED_IMAGES', True)
    
    @property
    def image_dir(self) -> str:
        """图片保存目录"""
        return self.get('EXTRACTED_IMAGES_DIR', 'extracted_figures')


# 全局配置实例
_global_config = Config()


def get_config(reload: bool = False) -> Config:
    """
    获取全局配置实例
    
    参数:
        reload: 是否重新加载配置
    
    返回:
        Config实例
    """
    if reload:
        _global_config._loaded = False
    return _global_config


def load_config(config_file: str = None) -> Config:
    """
    加载配置文件
    
    参数:
        config_file: 配置文件路径（可选）
    
    返回:
        Config实例
    """
    config = get_config()
    config.load(config_file)
    return config


# 便捷函数
def get_api_key(default: str = None) -> Optional[str]:
    """获取API密钥"""
    config = get_config()
    return config.api_key or default


def get_api_config() -> Dict:
    """获取API配置字典"""
    config = get_config()
    return {
        'api_key': config.api_key,
        'api_base': config.api_base,
        'model': config.model
    }


if __name__ == '__main__':
    # 测试配置加载
    print("=" * 60)
    print("配置加载测试")
    print("=" * 60)
    print()
    
    config = load_config()
    
    print("配置项:")
    print(f"  API密钥: {config.api_key[:20]}..." if config.api_key else "  API密钥: 未设置")
    print(f"  API基础URL: {config.api_base}")
    print(f"  模型名称: {config.model}")
    print(f"  启用内容检测: {config.enable_content_check}")
    print(f"  保存图片: {config.save_images}")
    print(f"  图片目录: {config.image_dir}")
    print()
    
    if not config.api_key:
        print("⚠️  请先配置API密钥:")
        print("  1. 复制 config_api.example.py 为 config_api.py")
        print("  2. 在 config_api.py 中填入您的API密钥")





