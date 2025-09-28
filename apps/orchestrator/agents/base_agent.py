"""
Autonomous Multi-Agent System for Web Development
Each agent has specific responsibilities and can iterate until completion
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import time
from pathlib import Path

class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working" 
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING_FOR_FEEDBACK = "waiting_for_feedback"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class AgentTask:
    id: str
    type: str
    priority: TaskPriority
    input_data: Dict[str, Any]
    requirements: List[str]
    expected_output: Dict[str, Any]
    created_at: float
    deadline: Optional[float] = None
    dependencies: List[str] = None
    
class AgentResult:
    def __init__(self, success: bool, data: Dict[str, Any], 
                 issues: List[str] = None, suggestions: List[str] = None):
        self.success = success
        self.data = data
        self.issues = issues or []
        self.suggestions = suggestions or []
        self.timestamp = time.time()
        self.needs_improvement = len(self.issues) > 0

class BaseAgent(ABC):
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.current_task: Optional[AgentTask] = None
        self.completed_tasks: List[str] = []
        self.failure_count = 0
        self.max_retries = 3
        
    @abstractmethod
    def can_handle(self, task: AgentTask) -> bool:
        """Check if this agent can handle the given task"""
        pass
        
    @abstractmethod
    def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute the assigned task"""
        pass
    
    @abstractmethod
    def improve_result(self, result: AgentResult, feedback: Dict[str, Any]) -> AgentResult:
        """Improve previous result based on feedback"""
        pass
    
    def start_task(self, task: AgentTask) -> bool:
        if self.status != AgentStatus.IDLE:
            return False
        
        if not self.can_handle(task):
            return False
            
        self.current_task = task
        self.status = AgentStatus.WORKING
        return True
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.value,
            "current_task": self.current_task.id if self.current_task else None,
            "completed_tasks": len(self.completed_tasks),
            "failure_count": self.failure_count,
            "capabilities": self.capabilities
        }

class AgentWorkflow:
    """Manages the workflow between agents with autonomous feedback loops"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue: List[AgentTask] = []
        self.completed_tasks: Dict[str, AgentResult] = {}
        self.workflow_state = "idle"
        self.max_iterations = 5  # Max iterations for improvement
        
    def register_agent(self, agent: BaseAgent):
        """Register an agent in the system"""
        self.agents[agent.name] = agent
        
    def create_task(self, task_type: str, priority: TaskPriority, 
                   input_data: Dict[str, Any], requirements: List[str],
                   dependencies: List[str] = None) -> str:
        """Create a new task"""
        task_id = f"{task_type}_{int(time.time() * 1000)}"
        task = AgentTask(
            id=task_id,
            type=task_type,
            priority=priority,
            input_data=input_data,
            requirements=requirements,
            dependencies=dependencies or [],
            created_at=time.time()
        )
        self.task_queue.append(task)
        return task_id
    
    def find_suitable_agent(self, task: AgentTask) -> Optional[BaseAgent]:
        """Find the most suitable agent for a task"""
        available_agents = [
            agent for agent in self.agents.values() 
            if agent.status == AgentStatus.IDLE and agent.can_handle(task)
        ]
        
        if not available_agents:
            return None
            
        # Prefer agents with fewer failures
        return min(available_agents, key=lambda a: a.failure_count)
    
    def execute_autonomous_workflow(self, initial_requirements: str) -> Dict[str, Any]:
        """Execute complete autonomous workflow from requirements to final product"""
        
        # Phase 1: Requirements Analysis
        req_task_id = self.create_task(
            "analyze_requirements",
            TaskPriority.CRITICAL,
            {"user_input": initial_requirements},
            ["clear_specifications", "feature_list", "technical_requirements"]
        )
        
        workflow_results = {}
        current_iteration = 0
        
        while current_iteration < self.max_iterations:
            current_iteration += 1
            print(f"=== Iteration {current_iteration} ===")
            
            # Execute all pending tasks
            self._process_task_queue()
            
            # Check if we have any results that need improvement
            needs_improvement = self._check_for_improvements()
            
            if not needs_improvement:
                print("All tasks completed successfully!")
                break
                
            # Create improvement tasks based on feedback
            self._create_improvement_tasks()
            
        return {
            "success": current_iteration < self.max_iterations,
            "iterations": current_iteration,
            "results": self.completed_tasks,
            "final_output": self._generate_final_output()
        }
    
    def _process_task_queue(self):
        """Process all tasks in the queue"""
        while self.task_queue:
            # Sort by priority and dependencies
            self.task_queue.sort(key=lambda t: (t.priority.value, t.created_at), reverse=True)
            
            task = self.task_queue.pop(0)
            
            # Check if dependencies are met
            if not self._dependencies_met(task):
                self.task_queue.append(task)  # Put back at the end
                continue
            
            # Find and assign agent
            agent = self.find_suitable_agent(task)
            if not agent:
                print(f"No suitable agent found for task {task.id}")
                continue
            
            print(f"Assigning task {task.id} to agent {agent.name}")
            
            if agent.start_task(task):
                result = agent.execute_task(task)
                self.completed_tasks[task.id] = result
                agent.status = AgentStatus.IDLE
                agent.current_task = None
                
                if result.success:
                    agent.completed_tasks.append(task.id)
                else:
                    agent.failure_count += 1
                    
                print(f"Task {task.id} completed with success: {result.success}")
    
    def _dependencies_met(self, task: AgentTask) -> bool:
        """Check if all task dependencies are completed successfully"""
        if not task.dependencies:
            return True
            
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False
            if not self.completed_tasks[dep_id].success:
                return False
                
        return True
    
    def _check_for_improvements(self) -> bool:
        """Check if any completed tasks need improvement"""
        return any(
            result.needs_improvement 
            for result in self.completed_tasks.values()
        )
    
    def _create_improvement_tasks(self):
        """Create improvement tasks based on feedback"""
        for task_id, result in self.completed_tasks.items():
            if result.needs_improvement and result.issues:
                # Create improvement task
                improvement_task_id = self.create_task(
                    f"improve_{task_id}",
                    TaskPriority.HIGH,
                    {
                        "original_result": result.data,
                        "issues": result.issues,
                        "suggestions": result.suggestions
                    },
                    ["improved_output", "issue_resolution"]
                )
                print(f"Created improvement task: {improvement_task_id}")
    
    def _generate_final_output(self) -> Dict[str, Any]:
        """Generate the final deliverable from all completed tasks"""
        final_files = {}
        metadata = {
            "created_at": time.time(),
            "total_tasks": len(self.completed_tasks),
            "agents_used": list(set(
                result.data.get("agent_name", "unknown") 
                for result in self.completed_tasks.values()
            ))
        }
        
        # Combine all file outputs
        for result in self.completed_tasks.values():
            if "files" in result.data:
                final_files.update(result.data["files"])
        
        return {
            "files": final_files,
            "metadata": metadata,
            "quality_score": self._calculate_quality_score()
        }
    
    def _calculate_quality_score(self) -> float:
        """Calculate overall quality score based on task results"""
        if not self.completed_tasks:
            return 0.0
            
        total_score = 0
        total_tasks = 0
        
        for result in self.completed_tasks.values():
            if result.success:
                # Base score for success
                score = 70
                # Bonus for no issues
                if not result.issues:
                    score += 30
                # Penalty for issues
                else:
                    score -= len(result.issues) * 5
                    
                total_score += max(0, min(100, score))
            else:
                total_score += 0
                
            total_tasks += 1
        
        return total_score / total_tasks if total_tasks > 0 else 0.0