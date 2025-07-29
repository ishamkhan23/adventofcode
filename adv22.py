import re

# Represents a 3D cuboid with a sign +1 for on -1 for off with overlap
class Cuboid:
    def __init__(self, x_range, y_range, z_range, sign):
        self.x_range = x_range  # start, end for x
        self.y_range = y_range  
        self.z_range = z_range  
        self.sign = sign        # +1 if on, -1 if overlap subtraction

    def volume(self):
        # volume of this cuboid
        dx = self.x_range[1] - self.x_range[0] + 1
        dy = self.y_range[1] - self.y_range[0] + 1
        dz = self.z_range[1] - self.z_range[0] + 1
        return dx * dy * dz * self.sign

    def intersect(self, other):
        # overlapping cuboid 
        x1 = max(self.x_range[0], other.x_range[0])
        x2 = min(self.x_range[1], other.x_range[1])
        y1 = max(self.y_range[0], other.y_range[0])
        y2 = min(self.y_range[1], other.y_range[1])
        z1 = max(self.z_range[0], other.z_range[0])
        z2 = min(self.z_range[1], other.z_range[1])
        # If any dimension does not overlap, return None
        if x1 > x2 or y1 > y2 or z1 > z2:
            return None
        # Return the overlapping cuboid, with sign flipped to handle inclusion/exclusion
        return Cuboid((x1, x2), (y1, y2), (z1, z2), -self.sign)

def parse_instruction(line):
    action, coords = line.strip().split(" ")
    ranges = list(map(int, re.findall(r"-?\d+", coords)))
    x_range = (ranges[0], ranges[1])
    y_range = (ranges[2], ranges[3])
    z_range = (ranges[4], ranges[5])
    return action, Cuboid(x_range, y_range, z_range, 1)

def process_reboot_steps(lines):
    cuboids = []  # List of all cuboids 
    for line in lines:
        action, new_cuboid = parse_instruction(line)
        additions = []
        for existing in cuboids:
            overlap = existing.intersect(new_cuboid)
            if overlap:
                additions.append(overlap)  # Flip sign to handle overlap
        if action == "on":
            additions.append(new_cuboid)  # Include the new cuboid if turning on
        cuboids.extend(additions)  # Add all changes positive or negative
    return sum(c.volume() for c in cuboids)  

# Run the script
if __name__ == "__main__":
    with open("adv22.txt") as f:
        lines = f.readlines()
    result = process_reboot_steps(lines)
    print("Total cubes on after reboot:", result)
