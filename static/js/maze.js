class MazeBall {
    constructor(x, y, direction, speed) {
        this.x = x;
        this.y = y;
        this.direction = direction; // angle in radians
        this.speed = speed;
        this.element = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        this.element.setAttribute("class", "maze-ball");
        this.element.setAttribute("cx", x);
        this.element.setAttribute("cy", y);
    }

    move(maze) {
        const nextX = this.x + Math.cos(this.direction) * this.speed;
        const nextY = this.y + Math.sin(this.direction) * this.speed;

        // Check collision with maze walls
        if (this.checkCollision(nextX, nextY, maze)) {
            // Reflect direction (add some randomness)
            this.direction = this.direction + Math.PI + (Math.random() - 0.5);
        } else {
            this.x = nextX;
            this.y = nextY;
        }

        // Keep within bounds
        if (this.x < 0) this.x = maze.width;
        if (this.x > maze.width) this.x = 0;
        if (this.y < 0) this.y = maze.height;
        if (this.y > maze.height) this.y = 0;

        this.element.setAttribute("cx", this.x);
        this.element.setAttribute("cy", this.y);
    }

    checkCollision(x, y, maze) {
        // Simple collision detection with maze walls
        const pixel = maze.getContext('2d').getImageData(x, y, 1, 1).data;
        return pixel[3] > 0; // Check alpha channel
    }
}

class Maze {
    constructor() {
        this.svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        this.svg.setAttribute("class", "maze-background");
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.svg.setAttribute("viewBox", `0 0 ${this.width} ${this.height}`);
        
        // Add glow filter
        const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
        defs.innerHTML = `
            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        `;
        this.svg.appendChild(defs);

        this.generateMaze();
        this.balls = this.createBalls(50); // Create 50 balls

        document.body.appendChild(this.svg);
        this.animate();
    }

    generateMaze() {
        const cellSize = 50;
        const cols = Math.ceil(this.width / cellSize);
        const rows = Math.ceil(this.height / cellSize);

        for (let i = 0; i < cols; i++) {
            for (let j = 0; j < rows; j++) {
                if (Math.random() > 0.7) { // 30% chance to create a path
                    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    path.setAttribute("class", "maze-path");
                    
                    // Create random path segments
                    const x = i * cellSize;
                    const y = j * cellSize;
                    const d = this.generatePathSegment(x, y, cellSize);
                    path.setAttribute("d", d);
                    
                    this.svg.appendChild(path);
                }
            }
        }
    }

    generatePathSegment(x, y, size) {
        const type = Math.floor(Math.random() * 4);
        switch (type) {
            case 0: // Horizontal line
                return `M ${x} ${y + size/2} L ${x + size} ${y + size/2}`;
            case 1: // Vertical line
                return `M ${x + size/2} ${y} L ${x + size/2} ${y + size}`;
            case 2: // Curve 1
                return `M ${x} ${y} Q ${x + size/2} ${y + size/2} ${x + size} ${y + size}`;
            case 3: // Curve 2
                return `M ${x} ${y + size} Q ${x + size/2} ${y + size/2} ${x + size} ${y}`;
        }
    }

    createBalls(count) {
        const balls = [];
        for (let i = 0; i < count; i++) {
            const x = Math.random() * this.width;
            const y = Math.random() * this.height;
            const direction = Math.random() * Math.PI * 2;
            const speed = 1 + Math.random() * 2;
            
            const ball = new MazeBall(x, y, direction, speed);
            this.svg.appendChild(ball.element);
            balls.push(ball);
        }
        return balls;
    }

    animate() {
        this.balls.forEach(ball => ball.move(this));
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize maze when document is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Maze();
}); 