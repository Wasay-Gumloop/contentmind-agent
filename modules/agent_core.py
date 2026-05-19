"""
ContentMind AI — Agent Core
The master orchestrator — initializes and connects all modules.
"""
import logging
from modules.researcher    import Researcher
from modules.writer        import ContentWriter
from modules.visual_engine import VisualEngine
from modules.poster        import Poster
from modules.scheduler     import Scheduler
from modules.brain         import AgentBrain
from modules.memory        import AgentMemory
from config import Config

logger = logging.getLogger("ContentMind.Core")


class ContentMindAgent:
    """
    The master autonomous agent.
    Pipeline: Research → Write → Visualize → Post → Remember → Learn
    """

    def __init__(self):
        Config.validate()
        logger.info("Initializing ContentMind Agent...")

        self.memory        = AgentMemory()
        self.researcher    = Researcher()
        self.writer        = ContentWriter()
        self.visual_engine = VisualEngine()
        self.poster        = Poster()
        self.scheduler     = Scheduler()
        self.brain         = AgentBrain(memory=self.memory)

        logger.info("ContentMind Agent ready.")
        print(f"""
╔══════════════════════════════════════════╗
║   ContentMind AI — Agent Initialized     ║
║   Brand   : {Config.BRAND_NAME:<30}║
║   Niche   : {Config.NICHE[:30]:<30}║
║   Model   : {Config.AI_MODEL:<30}║
║   Dry Run : {str(Config.DRY_RUN):<30}║
╚══════════════════════════════════════════╝
        """)

    def status(self):
        return {
            "brand"       : Config.BRAND_NAME,
            "niche"       : Config.NICHE,
            "model"       : Config.AI_MODEL,
            "dry_run"     : Config.DRY_RUN,
            "memory_runs" : len(self.memory.total_runs()),
        }
