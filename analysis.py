# Healthcare Dataset Analysis
# Author: Marcus Mitchell
# Description: Exploratory data analysis of patient healthcare records
# covering billing trends, medical conditions, insurance providers,
# and admission patterns across 55,500 patient records.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Configuration ────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2", "#937860"]
FILE = "healthcare_dataset.csv"

# ── 1. Load & Clean ──────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv(FILE)
print(f"  Loaded {len(df):,} records | {df.shape[1]} columns")

# Fix inconsistent name capitalization (e.g. "Bobby JacksOn" → "Bobby Jackson")
df["Name"] = df["Name"].str.title()

# Parse dates
df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
df["Discharge Date"] = pd.to_datetime(df["Discharge Date"])

# Calculate length of stay in days
df["Length of Stay"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days

# Flag negative billing amounts as data quality issues
df["Billing Flag"] = df["Billing Amount"] < 0
n_negative = df["Billing Flag"].sum()
if n_negative > 0:
    print(f"  ⚠ Data quality: {n_negative} records with negative billing amounts flagged")

# Remove negative billing for analysis
df_clean = df[df["Billing Amount"] >= 0].copy()
print(f"  Clean records for analysis: {len(df_clean):,}\n")

# ── 2. Summary Stats ─────────────────────────────────────────────
print("=" * 55)
print("SUMMARY")
print("=" * 55)
print(f"  Age range:          {df_clean['Age'].min()} – {df_clean['Age'].max()} yrs")
print(f"  Avg age:            {df_clean['Age'].mean():.1f} yrs")
print(f"  Avg billing amount: ${df_clean['Billing Amount'].mean():,.2f}")
print(f"  Avg length of stay: {df_clean['Length of Stay'].mean():.1f} days")
print(f"  Medical conditions: {df_clean['Medical Condition'].nunique()}")
print(f"  Hospitals:          {df_clean['Hospital'].nunique()}")
print(f"  Doctors:            {df_clean['Doctor'].nunique()}")
print()

# ── 3. Visualizations ────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle("Healthcare Dataset — Exploratory Analysis\nMarcus Mitchell", 
             fontsize=16, fontweight="bold", y=1.01)

# -- Plot 1: Medical Condition Distribution
ax1 = axes[0, 0]
condition_counts = df_clean["Medical Condition"].value_counts()
bars = ax1.barh(condition_counts.index, condition_counts.values, color=COLORS)
ax1.set_title("Patient Distribution by Medical Condition", fontweight="bold")
ax1.set_xlabel("Number of Patients")
for bar, val in zip(bars, condition_counts.values):
    ax1.text(bar.get_width() + 50, bar.get_y() + bar.get_height() / 2,
             f"{val:,}", va="center", fontsize=9)
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# -- Plot 2: Avg Billing by Medical Condition
ax2 = axes[0, 1]
avg_billing = df_clean.groupby("Medical Condition")["Billing Amount"].mean().sort_values(ascending=False)
bars2 = ax2.bar(avg_billing.index, avg_billing.values, color=COLORS)
ax2.set_title("Average Billing Amount by Condition", fontweight="bold")
ax2.set_ylabel("Average Billing ($)")
ax2.tick_params(axis="x", rotation=20)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x):,}"))
for bar, val in zip(bars2, avg_billing.values):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
             f"${val:,.0f}", ha="center", fontsize=8)

# -- Plot 3: Admission Type Breakdown
ax3 = axes[0, 2]
admission_counts = df_clean["Admission Type"].value_counts()
ax3.pie(admission_counts.values, labels=admission_counts.index,
        autopct="%1.1f%%", colors=COLORS, startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5})
ax3.set_title("Admission Type Breakdown", fontweight="bold")

# -- Plot 4: Billing by Insurance Provider
ax4 = axes[1, 0]
ins_billing = df_clean.groupby("Insurance Provider")["Billing Amount"].mean().sort_values(ascending=False)
bars4 = ax4.bar(ins_billing.index, ins_billing.values, color=COLORS)
ax4.set_title("Avg Billing Amount by Insurance Provider", fontweight="bold")
ax4.set_ylabel("Average Billing ($)")
ax4.tick_params(axis="x", rotation=15)
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x):,}"))
for bar, val in zip(bars4, ins_billing.values):
    ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 150,
             f"${val:,.0f}", ha="center", fontsize=8)

# -- Plot 5: Age Distribution
ax5 = axes[1, 1]
ax5.hist(df_clean["Age"], bins=30, color=COLORS[0], edgecolor="white", linewidth=0.6)
ax5.set_title("Patient Age Distribution", fontweight="bold")
ax5.set_xlabel("Age (years)")
ax5.set_ylabel("Number of Patients")
ax5.axvline(df_clean["Age"].mean(), color=COLORS[1], linestyle="--",
            linewidth=1.8, label=f"Mean: {df_clean['Age'].mean():.1f} yrs")
ax5.legend()

# -- Plot 6: Length of Stay by Admission Type
ax6 = axes[1, 2]
stay_data = [df_clean[df_clean["Admission Type"] == t]["Length of Stay"].dropna()
             for t in ["Elective", "Urgent", "Emergency"]]
bp = ax6.boxplot(stay_data, labels=["Elective", "Urgent", "Emergency"],
                 patch_artist=True, notch=False)
for patch, color in zip(bp["boxes"], COLORS):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax6.set_title("Length of Stay by Admission Type", fontweight="bold")
ax6.set_ylabel("Days")

plt.tight_layout()
plt.savefig("healthcare_analysis.png", dpi=150, bbox_inches="tight")
print("  Chart saved → healthcare_analysis.png")

# ── 4. Key Insights ──────────────────────────────────────────────
print()
print("=" * 55)
print("KEY INSIGHTS")
print("=" * 55)

highest_bill_condition = avg_billing.idxmax()
lowest_bill_condition = avg_billing.idxmin()
print(f"  Highest avg billing condition: {highest_bill_condition} (${avg_billing.max():,.2f})")
print(f"  Lowest avg billing condition:  {lowest_bill_condition} (${avg_billing.min():,.2f})")

highest_ins = ins_billing.idxmax()
lowest_ins = ins_billing.idxmin()
print(f"  Highest avg billing insurer:   {highest_ins} (${ins_billing.max():,.2f})")
print(f"  Lowest avg billing insurer:    {lowest_ins} (${ins_billing.min():,.2f})")

stay_by_type = df_clean.groupby("Admission Type")["Length of Stay"].mean()
print(f"\n  Avg length of stay:")
for t, d in stay_by_type.items():
    print(f"    {t}: {d:.1f} days")

test_result_pct = df_clean["Test Results"].value_counts(normalize=True) * 100
print(f"\n  Test result breakdown:")
for r, p in test_result_pct.items():
    print(f"    {r}: {p:.1f}%")

print()
print("Analysis complete.")
