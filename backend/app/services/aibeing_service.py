from app.extensions import db
from app.models.aibeing import AIBeing
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class AIBeingService:
    """数字人服务类，提供数字人相关的业务逻辑"""
    
    @staticmethod
    def get_all_aibeings(page: int = 1, per_page: int = 20, 
                       filters: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict], int, int]:
        """
        获取数字人列表
        
        Args:
            page: 页码，从1开始
            per_page: 每页数量
            filters: 过滤条件，例如 {'type': 'video', 'status': 'active'}
            
        Returns:
            包含三个元素的元组：(数字人列表, 总页数, 总记录数)
        """
        try:
            query = AIBeing.query
            
            # 应用筛选条件
            if filters:
                for key, value in filters.items():
                    if hasattr(AIBeing, key) and value is not None:
                        query = query.filter(getattr(AIBeing, key) == value)
            
            # 计算总记录数
            total_count = query.count()
            # 计算总页数
            total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1
            
            # 分页并获取结果
            aibeings = query.order_by(AIBeing.created_at.desc()) \
                           .offset((page - 1) * per_page) \
                           .limit(per_page).all()
            
            # 转换为字典列表
            aibeings_list = [aibeing.to_dict() for aibeing in aibeings]
            
            return aibeings_list, total_pages, total_count
            
        except SQLAlchemyError as e:
            logger.error(f"获取数字人列表时发生错误: {str(e)}")
            raise
    
    @staticmethod
    def get_aibeing_by_id(aibeing_id: int) -> Optional[Dict]:
        """
        根据ID获取数字人详情
        
        Args:
            aibeing_id: 数字人ID
            
        Returns:
            数字人详情字典，如果不存在则返回None
        """
        try:
            aibeing = AIBeing.query.get(aibeing_id)
            return aibeing.to_dict() if aibeing else None
        except SQLAlchemyError as e:
            logger.error(f"获取数字人详情时发生错误: {str(e)}")
            raise
    
    @staticmethod
    def create_aibeing(data: Dict[str, Any]) -> Dict:
        """
        创建新的数字人
        
        Args:
            data: 数字人数据字典
            
        Returns:
            新创建的数字人详情字典
        """
        try:
            aibeing = AIBeing(**data)
            db.session.add(aibeing)
            db.session.commit()
            return aibeing.to_dict()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"创建数字人时发生错误: {str(e)}")
            raise
    
    @staticmethod
    def update_aibeing(aibeing_id: int, data: Dict[str, Any]) -> Optional[Dict]:
        """
        更新数字人信息
        
        Args:
            aibeing_id: 数字人ID
            data: 需要更新的数据字典
            
        Returns:
            更新后的数字人详情字典，如果不存在则返回None
        """
        try:
            aibeing = AIBeing.query.get(aibeing_id)
            if not aibeing:
                return None
                
            for key, value in data.items():
                if hasattr(aibeing, key):
                    setattr(aibeing, key, value)
            
            db.session.commit()
            return aibeing.to_dict()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"更新数字人时发生错误: {str(e)}")
            raise
    
    @staticmethod
    def delete_aibeing(aibeing_id: int) -> bool:
        """
        删除数字人
        
        Args:
            aibeing_id: 数字人ID
            
        Returns:
            操作是否成功
        """
        try:
            aibeing = AIBeing.query.get(aibeing_id)
            if not aibeing:
                return False
                
            db.session.delete(aibeing)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"删除数字人时发生错误: {str(e)}")
            raise 