"""
SUMA GUI Styles
Centralized style management
"""

from .colors import SumaColors

class SumaStyles:
    """מחלקה מרכזית לסגנונות"""
    
    @staticmethod
    def get_main_stylesheet():
        """סגנון ראשי לאפליקציה"""
        return f"""
        QMainWindow {{
            background-color: {SumaColors.GENERAL_BG};
            color: {SumaColors.TEXT_PRIMARY};
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 14px;
        }}
        
        QPushButton {{
            background-color: {SumaColors.BUTTON_NORMAL_BG};
            color: {SumaColors.BUTTON_NORMAL_TEXT};
            border: 2px solid {SumaColors.BUTTON_NORMAL_BORDER};
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            min-height: 36px;
            min-width: 120px;
        }}
        
        QPushButton:hover {{
            background-color: {SumaColors.BUTTON_HOVER_BG};
        }}
        
        QPushButton:pressed {{
            background-color: {SumaColors.BUTTON_PRESSED_BG};
        }}
        
        QPushButton:disabled {{
            background-color: {SumaColors.TEXT_SECONDARY};
            color: {SumaColors.WHITE};
            border-color: {SumaColors.TEXT_SECONDARY};
        }}
        
        QLineEdit {{
            background-color: {SumaColors.WHITE};
            border: 2px solid {SumaColors.FIELD_BORDER};
            border-radius: 4px;
            padding: 8px;
            color: {SumaColors.TEXT_PRIMARY};
        }}
        
        QLineEdit:focus {{
            border-color: {SumaColors.BRAND_BLUE};
        }}
        
        QLabel {{
            color: {SumaColors.TEXT_PRIMARY};
            text-align: center;
        }}
        
        QProgressBar {{
            background-color: {SumaColors.IMAGE_DISPLAY_BG};
            border: 1px solid {SumaColors.FIELD_BORDER};
            border-radius: 4px;
            text-align: center;
            font-weight: bold;
            min-height: 20px;
            color: {SumaColors.TEXT_PRIMARY};
        }}
        
        QProgressBar::chunk {{
            background-color: {SumaColors.LIGHT_BLUE};
            border-radius: 3px;
        }}
        
        QTreeWidget {{
            background-color: {SumaColors.WHITE};
            border: 1px solid {SumaColors.FIELD_BORDER};
            border-radius: 4px;
            color: {SumaColors.TEXT_PRIMARY};
            outline: 0;
        }}
        
        QTreeWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {SumaColors.IMAGE_DISPLAY_BG};
        }}
        
        QTreeWidget::item:selected {{
            background-color: {SumaColors.BUTTON_HOVER_BG};
            color: {SumaColors.TEXT_PRIMARY};
        }}
        
        QTreeWidget::item:hover {{
            background-color: {SumaColors.GENERAL_BG};
        }}
        
        QHeaderView::section {{
            background-color: {SumaColors.IMAGE_DISPLAY_BG};
            color: {SumaColors.TEXT_PRIMARY};
            padding: 8px;
            border: none;
            border-right: 1px solid {SumaColors.FIELD_BORDER};
            font-weight: bold;
        }}
        """
    
    @staticmethod
    def get_primary_button_style():
        """סגנון כפתור ראשי (כחול)"""
        return f"""
        QPushButton {{
            background-color: {SumaColors.BRAND_BLUE};
            color: {SumaColors.TEXT_ON_DARK};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {SumaColors.LIGHT_BLUE};
        }}
        
        QPushButton:pressed {{
            background-color: {SumaColors.LIGHT_BLUE};
        }}
        """
    
    @staticmethod
    def get_main_title_style():
        return f"""
        QLabel {{
            color: {SumaColors.BRAND_BLUE};
            font-size: 96px;
            font-weight: bold;
            padding: 20px;
            text-align: center;
            letter-spacing: 6px;
        }}
        """
    
    @staticmethod
    def get_title_style():
        return f"""
        QLabel {{
            color: {SumaColors.TEXT_PRIMARY};
            font-size: 48px;
            font-weight: bold;
            padding: 20px;
            text-align: center;
        }}
        """
    
    @staticmethod
    def get_subtitle_style():
        """סגנון כותרות משנה"""
        return f"""
        QLabel {{
            color: {SumaColors.TEXT_SECONDARY};
            font-size: 14px;
            padding: 5px;
            text-align: center;
        }}
        """
    
    @staticmethod
    def get_tree_widget_style():
        """סגנון ספציפי ל-tree widget עם יישור שמאל"""
        return f"""
        QTreeWidget {{
            background-color: {SumaColors.WHITE};
            border: 1px solid {SumaColors.FIELD_BORDER};
            border-radius: 4px;
            color: {SumaColors.TEXT_PRIMARY};
            outline: 0;
            text-align: left;
        }}
        
        QTreeWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {SumaColors.IMAGE_DISPLAY_BG};
            text-align: left;
        }}
        
        QTreeWidget::item:selected {{
            background-color: {SumaColors.BUTTON_HOVER_BG};
            color: {SumaColors.TEXT_PRIMARY};
        }}
        
        QTreeWidget::item:hover {{
            background-color: {SumaColors.GENERAL_BG};
        }}
        
        QHeaderView::section {{
            background-color: {SumaColors.IMAGE_DISPLAY_BG};
            color: {SumaColors.TEXT_PRIMARY};
            padding: 8px;
            border: none;
            border-right: 1px solid {SumaColors.FIELD_BORDER};
            font-weight: bold;
            text-align: left;
        }}
        """ 