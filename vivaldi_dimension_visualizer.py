"""
Vivaldi Antenna - Detailed Dimension Visualization
Creates annotated diagrams showing all key parts and measurements
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from vivaldi_calculator import VivaldiCalculator, VivaldiAntennaSpecs


class VivaldiDimensionVisualizer:
    """Creates detailed dimension diagrams for Vivaldi antenna"""
    
    def __init__(self):
        specs = VivaldiAntennaSpecs(
            min_freq=400,      # 400 MHz
            max_freq=7000,     # 7 GHz
            dielectric_constant=1.0,
            feed_impedance=50.0
        )
        self.calculator = VivaldiCalculator(specs)
    
    def create_labeled_antenna_diagram(self):
        """Create detailed labeled antenna diagram with all dimensions"""
        
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        
        # Calculate antenna dimensions
        lambda_center = self.calculator.wavelength_at_freq(self.calculator.center_freq)
        antenna_length = self.calculator.calculate_antenna_length(self.calculator.center_freq, 0.4)
        slot_width_min = self.calculator.slot_width(400)
        slot_width_max = self.calculator.slot_width(7000) * 4
        
        # Generate exponential profile
        x_coords, y_upper, y_lower = self.calculator.exponential_taper_profile(
            antenna_length,
            slot_width_min,
            slot_width_max,
            num_points=300
        )
        
        # Draw antenna profile
        ax.plot(x_coords, y_upper, 'b-', linewidth=3, label='Antenna edges')
        ax.plot(x_coords, y_lower, 'b-', linewidth=3)
        ax.fill_between(x_coords, y_upper, y_lower, alpha=0.2, color='blue')
        
        # Add substrate boundary (larger than antenna)
        substrate_width = slot_width_min * 6
        substrate_length = antenna_length * 1.1
        substrate_margin = (substrate_width - slot_width_max * 2) / 2
        
        rect_substrate = FancyBboxPatch(
            (-5, -substrate_width/2), substrate_length + 10, substrate_width,
            boxstyle="round,pad=2", edgecolor='black', facecolor='lightyellow', 
            linewidth=2, linestyle='--', alpha=0.3
        )
        ax.add_patch(rect_substrate)
        
        # Add dimension arrows and labels
        arrow_y = -substrate_width/2 - 8
        
        # 1. ANTENNA LENGTH
        arrow = FancyArrowPatch(
            (0, arrow_y), (antenna_length, arrow_y),
            arrowstyle='<->', mutation_scale=25, color='red', linewidth=2.5
        )
        ax.add_patch(arrow)
        ax.text(antenna_length/2, arrow_y - 3, 
                f'ANTENNA LENGTH\n{antenna_length:.1f} mm', 
                ha='center', fontsize=12, fontweight='bold', color='red',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
        
        # 2. SLOT WIDTH AT START (400 MHz)
        arrow_slot_start = FancyArrowPatch(
            (-3, -slot_width_min/2), (-3, slot_width_min/2),
            arrowstyle='<->', mutation_scale=20, color='green', linewidth=2
        )
        ax.add_patch(arrow_slot_start)
        ax.text(-8, 0, 
                f'SLOT WIDTH\n@ 400 MHz\n{slot_width_min:.3f} mm', 
                ha='right', fontsize=10, fontweight='bold', color='green',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        
        # 3. SLOT WIDTH AT END (7 GHz equivalent)
        arrow_slot_end = FancyArrowPatch(
            (antenna_length + 3, -slot_width_max/2), (antenna_length + 3, slot_width_max/2),
            arrowstyle='<->', mutation_scale=20, color='orange', linewidth=2
        )
        ax.add_patch(arrow_slot_end)
        ax.text(antenna_length + 8, 0, 
                f'SLOT WIDTH\n@ 7 GHz\n{slot_width_max:.2f} mm', 
                ha='left', fontsize=10, fontweight='bold', color='orange',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        # 4. SUBSTRATE WIDTH
        arrow_sub_width = FancyArrowPatch(
            (antenna_length + 15, -substrate_width/2), (antenna_length + 15, substrate_width/2),
            arrowstyle='<->', mutation_scale=25, color='purple', linewidth=2.5
        )
        ax.add_patch(arrow_sub_width)
        ax.text(antenna_length + 22, 0, 
                f'SUBSTRATE WIDTH\n{substrate_width:.1f} mm', 
                ha='left', fontsize=11, fontweight='bold', color='purple',
                bbox=dict(boxstyle='round', facecolor='plum', alpha=0.8))
        
        # 5. SUBSTRATE THICKNESS (show as side view indicator)
        ax.text(antenna_length/2, substrate_width/2 + 3, 
                f'THICKNESS: 1.6 mm (Standard FR4)', 
                ha='center', fontsize=10, fontweight='bold', color='darkblue',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # 6. FEED POINT (SMA connector)
        feed_circle = patches.Circle((0, 0), 1, color='red', zorder=5)
        ax.add_patch(feed_circle)
        ax.text(-2, -3, 'SMA\nCONNECTOR\n(50Ω)', 
                ha='right', fontsize=9, fontweight='bold', color='red',
                bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.9))
        
        # 7. GROUND PLANE indicator
        ax.text(antenna_length/2, -substrate_width/2 + 2, 
                'GROUND PLANE (Reverse Side)', 
                ha='center', fontsize=9, style='italic', color='darkred',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
        
        # Add frequency annotations at key points
        ax.text(0.1*antenna_length, -substrate_width/2 - 13, '400 MHz', 
                fontsize=9, ha='center', color='green', fontweight='bold')
        ax.text(0.5*antenna_length, -substrate_width/2 - 13, 'Center: 3.7 GHz', 
                fontsize=9, ha='center', color='blue', fontweight='bold')
        ax.text(0.9*antenna_length, -substrate_width/2 - 13, '7 GHz', 
                fontsize=9, ha='center', color='orange', fontweight='bold')
        
        # Title and labels
        ax.set_title('Vivaldi Antenna - Complete Dimension Diagram (400 MHz - 7 GHz)', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Length (mm)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Width (mm)', fontsize=12, fontweight='bold')
        
        # Set equal aspect and limits
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, alpha=0.2, linestyle='--')
        
        margin = 15
        ax.set_xlim(-margin, antenna_length + margin)
        ax.set_ylim(-substrate_width/2 - 20, substrate_width/2 + 10)
        
        plt.tight_layout()
        return fig
    
    def create_side_view_diagram(self):
        """Create side view showing thickness and substrate"""
        
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        
        antenna_length = self.calculator.calculate_antenna_length(self.calculator.center_freq, 0.4)
        substrate_length = antenna_length * 1.1
        substrate_thickness = 1.6
        
        # Draw substrate
        rect_substrate = patches.Rectangle(
            (0, 0), substrate_length, substrate_thickness,
            linewidth=3, edgecolor='black', facecolor='tan', alpha=0.6
        )
        ax.add_patch(rect_substrate)
        
        # Draw copper on top
        rect_copper = patches.Rectangle(
            (0, substrate_thickness), substrate_length, 0.035,
            linewidth=1, edgecolor='orange', facecolor='orange', alpha=0.8
        )
        ax.add_patch(rect_copper)
        
        # Draw copper on bottom (ground plane)
        rect_ground = patches.Rectangle(
            (0, -0.035), substrate_length, 0.035,
            linewidth=1, edgecolor='red', facecolor='red', alpha=0.8
        )
        ax.add_patch(rect_ground)
        
        # Add dimension arrows
        arrow_thick = FancyArrowPatch(
            (-2, 0), (-2, substrate_thickness),
            arrowstyle='<->', mutation_scale=25, color='blue', linewidth=2.5
        )
        ax.add_patch(arrow_thick)
        ax.text(-4, substrate_thickness/2, 
                f'PCB\nTHICKNESS\n1.6 mm', 
                ha='right', fontsize=11, fontweight='bold', color='blue',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        arrow_length = FancyArrowPatch(
            (0, substrate_thickness + 2), (substrate_length, substrate_thickness + 2),
            arrowstyle='<->', mutation_scale=25, color='red', linewidth=2.5
        )
        ax.add_patch(arrow_length)
        ax.text(substrate_length/2, substrate_thickness + 3.5, 
                f'SUBSTRATE LENGTH: {substrate_length:.1f} mm', 
                ha='center', fontsize=11, fontweight='bold', color='red',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        # Labels
        ax.text(substrate_length/2, substrate_thickness/2, 
                'FR4 Dielectric (εr=4.6)', 
                ha='center', va='center', fontsize=11, fontweight='bold', color='white',
                bbox=dict(boxstyle='round', facecolor='brown', alpha=0.7))
        
        ax.text(substrate_length/2, substrate_thickness + 0.02, 
                'Antenna Conductor (Top)', 
                ha='center', fontsize=9, fontweight='bold', color='white',
                bbox=dict(boxstyle='round', facecolor='darkorange', alpha=0.8))
        
        ax.text(substrate_length/2, -0.02, 
                'Ground Plane (Bottom)', 
                ha='center', fontsize=9, fontweight='bold', color='white',
                bbox=dict(boxstyle='round', facecolor='darkred', alpha=0.8))
        
        ax.set_title('Vivaldi Antenna - Side View (Cross Section)', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Length (mm)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Thickness (mm)', fontsize=12, fontweight='bold')
        
        ax.set_xlim(-6, substrate_length + 2)
        ax.set_ylim(-1.5, substrate_thickness + 5)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, alpha=0.2, linestyle='--')
        
        plt.tight_layout()
        return fig
    
    def create_component_labels_diagram(self):
        """Create diagram showing all components labeled"""
        
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        
        lambda_center = self.calculator.wavelength_at_freq(self.calculator.center_freq)
        antenna_length = self.calculator.calculate_antenna_length(self.calculator.center_freq, 0.4)
        slot_width_min = self.calculator.slot_width(400)
        slot_width_max = self.calculator.slot_width(7000) * 4
        
        # Generate profile
        x_coords, y_upper, y_lower = self.calculator.exponential_taper_profile(
            antenna_length,
            slot_width_min,
            slot_width_max,
            num_points=300
        )
        
        # Draw antenna
        ax.fill_between(x_coords, y_upper, y_lower, alpha=0.3, color='blue', label='Antenna Slot')
        ax.plot(x_coords, y_upper, 'b-', linewidth=3)
        ax.plot(x_coords, y_lower, 'b-', linewidth=3)
        
        # 1. SMA Connector
        connector_box = FancyBboxPatch(
            (-4, -1), 3, 2,
            boxstyle="round,pad=0.1", edgecolor='red', facecolor='red', 
            linewidth=2, alpha=0.7
        )
        ax.add_patch(connector_box)
        ax.annotate('SMA CONNECTOR\n(50Ω Feed)', xy=(0, 0), xytext=(-8, 3),
                    fontsize=11, fontweight='bold', color='red',
                    bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.9),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        # 2. Slot Opening (Feed Point)
        ax.annotate('SLOT OPENING\n(Feed Point)', xy=(0, slot_width_min/2 + 1), xytext=(8, 8),
                    fontsize=11, fontweight='bold', color='darkgreen',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9),
                    arrowprops=dict(arrowstyle='->', color='darkgreen', lw=2))
        
        # 3. Exponential Taper Region
        mid_x = antenna_length * 0.5
        mid_y = (y_upper[150] + y_lower[150]) / 2 + 5
        ax.annotate('EXPONENTIAL TAPER\n(Wideband Matching)', 
                    xy=(mid_x, 0), xytext=(mid_x - 5, mid_y),
                    fontsize=11, fontweight='bold', color='darkblue',
                    bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9),
                    arrowprops=dict(arrowstyle='->', color='darkblue', lw=2))
        
        # 4. Radiating Aperture (End)
        ax.annotate('RADIATING APERTURE\n(Wideband Radiation)', 
                    xy=(antenna_length, slot_width_max/2), xytext=(antenna_length - 8, slot_width_max/2 + 8),
                    fontsize=11, fontweight='bold', color='purple',
                    bbox=dict(boxstyle='round', facecolor='plum', alpha=0.9),
                    arrowprops=dict(arrowstyle='->', color='purple', lw=2))
        
        # 5. Substrate
        ax.annotate('FR4 SUBSTRATE\n1.6mm Thickness', 
                    xy=(antenna_length/2, -slot_width_min/2 - 5), xytext=(antenna_length/2, -12),
                    fontsize=11, fontweight='bold', color='darkred',
                    bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9),
                    arrowprops=dict(arrowstyle='->', color='darkred', lw=2))
        
        # 6. Ground Plane (indicate with hatching)
        ax.axhline(y=-slot_width_min/2 - 5, color='red', linestyle='--', linewidth=2, alpha=0.5)
        ax.annotate('GROUND PLANE\n(Bottom Side)', 
                    xy=(antenna_length * 0.25, -slot_width_min/2 - 5), xytext=(antenna_length * 0.25, -16),
                    fontsize=10, fontweight='bold', color='red', style='italic',
                    bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.8),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
        
        ax.set_title('Vivaldi Antenna - Component Labels & Structure', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Length (mm)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Width (mm)', fontsize=12, fontweight='bold')
        
        ax.set_xlim(-12, antenna_length + 5)
        ax.set_ylim(-20, 15)
        ax.grid(True, alpha=0.2, linestyle='--')
        
        plt.tight_layout()
        return fig
    
    def create_dimensions_table(self):
        """Create a detailed dimensions reference table"""
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('tight')
        ax.axis('off')
        
        # Get dimensions
        lambda_center = self.calculator.wavelength_at_freq(self.calculator.center_freq)
        antenna_length = self.calculator.calculate_antenna_length(self.calculator.center_freq, 0.4)
        slot_width_min = self.calculator.slot_width(400)
        slot_width_center = self.calculator.slot_width(self.calculator.center_freq)
        slot_width_max = self.calculator.slot_width(7000)
        
        table_data = [
            ['DIMENSION', 'VALUE', 'UNIT', 'DESCRIPTION'],
            ['', '', '', ''],
            ['ANTENNA LENGTH', f'{antenna_length:.2f}', 'mm', 'Total length of taper from feed to aperture'],
            ['ANTENNA WIDTH (START)', f'{slot_width_min:.3f}', 'mm', 'Slot width at feed point (400 MHz)'],
            ['ANTENNA WIDTH (CENTER)', f'{slot_width_center:.3f}', 'mm', 'Slot width at center frequency (3.7 GHz)'],
            ['ANTENNA WIDTH (END)', f'{slot_width_max:.3f}', 'mm', 'Slot width at high end (7 GHz)'],
            ['', '', '', ''],
            ['SUBSTRATE LENGTH', f'{antenna_length * 1.1:.2f}', 'mm', 'Length of PCB substrate'],
            ['SUBSTRATE WIDTH', f'{slot_width_min * 6:.2f}', 'mm', 'Width of PCB substrate'],
            ['SUBSTRATE THICKNESS', '1.6', 'mm', 'Standard FR4 PCB thickness'],
            ['', '', '', ''],\n            ['FEED LINE WIDTH', '2.0', 'mm', 'Microstrip width for 50Ω impedance'],\n            ['FEED LINE LENGTH', '5.0', 'mm', 'SMA connector to antenna transition'],\n            ['SMA PIN DIAMETER', '0.64', 'mm', 'Center pin diameter of SMA connector'],\n            ['', '', '', ''],\n            ['CENTER FREQUENCY', '3700', 'MHz', 'Geometric center of band'],\n            ['BANDWIDTH RATIO', '17.5:1', 'ratio', 'Maximum to minimum frequency ratio'],\n            ['TARGET IMPEDANCE', '50', 'Ohms', 'SMA connector impedance'],\n        ]\n        \n        table = ax.table(cellText=table_data, cellLoc='left', loc='center',\n                        colWidths=[0.25, 0.15, 0.1, 0.5])\n        \n        table.auto_set_font_size(False)\n        table.set_fontsize(10)\n        table.scale(1, 2.5)\n        \n        # Style header row\n        for i in range(4):\n            table[(0, i)].set_facecolor('#4472C4')\n            table[(0, i)].set_text_props(weight='bold', color='white', fontsize=11)\n        \n        # Alternate row colors\n        for i in range(1, len(table_data)):\n            for j in range(4):\n                if i == 1 or i == 6 or i == 13:  # Separator rows\n                    table[(i, j)].set_facecolor('#E7E6E6')\n                elif i % 2 == 0:\n                    table[(i, j)].set_facecolor('#D9E1F2')\n                else:\n                    table[(i, j)].set_facecolor('#F2F2F2')\n        \n        plt.title('Vivaldi Antenna - Dimensions Reference Table', \n                 fontsize=14, fontweight='bold', pad=20)\n        plt.tight_layout()\n        \n        return fig


# Generate all diagrams
if __name__ == \"__main__\":\n    visualizer = VivaldiDimensionVisualizer()\n    \n    print(\"Generating dimension diagrams...\\n\")\n    \n    # 1. Main labeled diagram\n    print(\"1. Creating main dimension diagram...\")\n    fig1 = visualizer.create_labeled_antenna_diagram()\n    fig1.savefig('01_Vivaldi_Dimensions_Full.png', dpi=300, bbox_inches='tight')\n    print(\"   ✓ Saved: 01_Vivaldi_Dimensions_Full.png\")\n    \n    # 2. Side view\n    print(\"2. Creating side view diagram...\")\n    fig2 = visualizer.create_side_view_diagram()\n    fig2.savefig('02_Vivaldi_SideView.png', dpi=300, bbox_inches='tight')\n    print(\"   ✓ Saved: 02_Vivaldi_SideView.png\")\n    \n    # 3. Component labels\n    print(\"3. Creating component labels diagram...\")\n    fig3 = visualizer.create_component_labels_diagram()\n    fig3.savefig('03_Vivaldi_Components.png', dpi=300, bbox_inches='tight')\n    print(\"   ✓ Saved: 03_Vivaldi_Components.png\")\n    \n    # 4. Dimensions table\n    print(\"4. Creating dimensions reference table...\")\n    fig4 = visualizer.create_dimensions_table()\n    fig4.savefig('04_Vivaldi_Dimensions_Table.png', dpi=300, bbox_inches='tight')\n    print(\"   ✓ Saved: 04_Vivaldi_Dimensions_Table.png\")\n    \n    print(\"\\n\" + \"=\"*70)\n    print(\"All dimension diagrams generated successfully!\")\n    print(\"=\"*70)\n    print(\"\\nGenerated files:\")\n    print(\"  • 01_Vivaldi_Dimensions_Full.png - Complete dimension diagram\")\n    print(\"  • 02_Vivaldi_SideView.png - Side/cross-section view\")\n    print(\"  • 03_Vivaldi_Components.png - Labeled components\")\n    print(\"  • 04_Vivaldi_Dimensions_Table.png - Dimensions reference table\")\n    \n    plt.show()
