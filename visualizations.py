"""
Visualization functions using Plotly for survey progress monitoring
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

class ProgressCharts:
    """Generate Plotly charts for survey progress monitoring"""
    
    # Vanuatu flag-inspired color scheme
    COLORS = {
        'completed': '#009543',      # Vanuatu Green
        'in_progress': '#FCD116',    # Vanuatu Yellow
        'pending': '#CE1126',        # Vanuatu Red
        'validated': '#000000',      # Black
        'primary': '#CE1126',        # Vanuatu Red
        'secondary': '#009543',      # Vanuatu Green
        'warning': '#F18F01',
        'danger': '#CE1126',
        'accent': '#FCD116',         # Vanuatu Yellow
    }
    
    @staticmethod
    def create_progress_gauge(completed, target):
        """Create gauge chart showing overall progress"""
        percentage = (completed / target * 100) if target > 0 else 0
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=completed,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Survey Progress<br><span style='font-size:0.8em'>Target: {target:,}</span>"},
            delta={'reference': target, 'increasing': {'color': ProgressCharts.COLORS['completed']}},
            number={'suffix': f" ({percentage:.1f}%)"},
            gauge={
                'axis': {'range': [None, target], 'tickwidth': 1},
                'bar': {'color': ProgressCharts.COLORS['completed']},
                'steps': [
                    {'range': [0, target * 0.25], 'color': '#FFE5E5'},
                    {'range': [target * 0.25, target * 0.5], 'color': '#FFD6AA'},
                    {'range': [target * 0.5, target * 0.75], 'color': '#C9F0E5'},
                    {'range': [target * 0.75, target], 'color': '#B8E6D5'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': target
                }
            }
        ))
        
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_daily_progress_chart(daily_data):
        """Create line chart showing daily survey progress"""
        fig = go.Figure()
        
        dates = daily_data.index.tolist()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=daily_data['total'],
            mode='lines+markers',
            name='Total Surveys',
            line=dict(color=ProgressCharts.COLORS['primary'], width=2),
            fill='tozeroy',
            fillcolor='rgba(46, 134, 171, 0.2)'
        ))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=daily_data['completed'],
            mode='lines+markers',
            name='Completed',
            line=dict(color=ProgressCharts.COLORS['completed'], width=2)
        ))
        
        fig.update_layout(
            title='Daily Survey Progress',
            xaxis_title='Date',
            yaxis_title='Number of Surveys',
            hovermode='x unified',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_status_distribution_chart(status_data):
        """Create pie chart for survey status distribution"""
        labels = list(status_data.keys())
        values = list(status_data.values())
        
        colors = {
            'Completed': ProgressCharts.COLORS['completed'],
            'Validated': ProgressCharts.COLORS['validated'],
            'In Progress': ProgressCharts.COLORS['in_progress'],
            'Pending Review': ProgressCharts.COLORS['pending']
        }
        
        chart_colors = [colors.get(label, ProgressCharts.COLORS['primary']) for label in labels]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=chart_colors),
            textinfo='label+percent+value',
            textposition='auto'
        )])
        
        fig.update_layout(
            title='Survey Status Distribution',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_province_progress_chart(province_data):
        """Create horizontal bar chart for province progress"""
        provinces = province_data.index.tolist()
        total = province_data['total_surveys'].tolist()
        completed = province_data['completed_surveys'].tolist()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=provinces,
            x=completed,
            name='Completed',
            orientation='h',
            marker=dict(color=ProgressCharts.COLORS['completed']),
            text=completed,
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            y=provinces,
            x=[t - c for t, c in zip(total, completed)],
            name='In Progress/Pending',
            orientation='h',
            marker=dict(color=ProgressCharts.COLORS['in_progress']),
            text=[t - c for t, c in zip(total, completed)],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Survey Progress by Province',
            xaxis_title='Number of Surveys',
            yaxis_title='Province',
            barmode='stack',
            height=400,
            showlegend=True
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_team_performance_chart(team_data):
        """Create bar chart for team performance"""
        teams = team_data.index.tolist()
        total = team_data['total_surveys'].tolist()
        completed = team_data['completed_surveys'].tolist()
        quality = team_data['quality_score'].tolist()
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Surveys by Team', 'Average Quality Score'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        fig.add_trace(
            go.Bar(
                x=teams,
                y=total,
                name='Total',
                marker_color=ProgressCharts.COLORS['primary'],
                text=total,
                textposition='auto'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=teams,
                y=completed,
                name='Completed',
                marker_color=ProgressCharts.COLORS['completed'],
                text=completed,
                textposition='auto'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=teams,
                y=quality,
                name='Quality',
                marker_color=ProgressCharts.COLORS['validated'],
                text=[f'{q:.1f}' if pd.notna(q) else 'N/A' for q in quality],
                textposition='auto',
                showlegend=False
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            height=450,
            showlegend=True
        )
        
        fig.update_yaxes(title_text="Number of Surveys", row=1, col=1)
        fig.update_yaxes(title_text="Quality Score (0-100)", row=1, col=2)
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_interviewer_leaderboard_chart(interviewer_data, top_n=15):
        """Create horizontal bar chart for top interviewers"""
        top_data = interviewer_data.head(top_n).reset_index()
        
        interviewers = [f"{row['interviewer_name']}" for idx, row in top_data.iterrows()]
        surveys = top_data['total_surveys'].tolist()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=interviewers[::-1],  # Reverse for better visualization
            x=surveys[::-1],
            orientation='h',
            marker=dict(
                color=surveys[::-1],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Surveys")
            ),
            text=surveys[::-1],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Total: %{x}<br><extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Top {top_n} Interviewers by Survey Count',
            xaxis_title='Number of Surveys',
            yaxis_title='Interviewer',
            height=500,
            margin=dict(l=150)
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_island_heatmap(island_data):
        """Create heatmap showing surveys by province and island"""
        # Pivot data for heatmap
        heatmap_data = island_data.reset_index()
        pivot = heatmap_data.pivot(index='island', columns='province', values='total_surveys')
        pivot = pivot.fillna(0)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='Blues',
            text=pivot.values,
            texttemplate='%{text:.0f}',
            textfont={"size": 10},
            colorbar=dict(title="Surveys")
        ))
        
        fig.update_layout(
            title='Survey Distribution by Province and Island',
            xaxis_title='Province',
            yaxis_title='Island',
            height=500
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_quality_trend_chart(df):
        """Create chart showing quality score trends over time"""
        df_quality = df[df['quality_score'].notna()].copy()
        df_quality['week'] = pd.to_datetime(df_quality['survey_date']).dt.to_period('W')
        
        weekly_quality = df_quality.groupby('week')['quality_score'].agg(['mean', 'count']).reset_index()
        weekly_quality['week'] = weekly_quality['week'].astype(str)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=weekly_quality['week'],
            y=weekly_quality['mean'],
            mode='lines+markers',
            name='Avg Quality Score',
            line=dict(color=ProgressCharts.COLORS['validated'], width=3),
            marker=dict(size=8),
            text=[f"Count: {c}" for c in weekly_quality['count']],
            hovertemplate='<b>Week %{x}</b><br>Avg Score: %{y:.1f}<br>%{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Weekly Quality Score Trend',
            xaxis_title='Week',
            yaxis_title='Average Quality Score',
            height=400,
            yaxis=dict(range=[0, 100])
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_time_efficiency_chart(team_data):
        """Create chart showing average time taken by team"""
        teams = team_data.index.tolist()
        avg_time = team_data['avg_duration_minutes'].tolist()
        
        fig = go.Figure(data=[
            go.Bar(
                x=teams,
                y=avg_time,
                marker_color=ProgressCharts.COLORS['warning'],
                text=[f'{t:.0f} min' for t in avg_time],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title='Average Survey Time by Team',
            xaxis_title='Team',
            yaxis_title='Average Time (minutes)',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_data_quality_chart(quality_metrics):
        """Create data quality metrics chart"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Quality Metrics', 'GPS & Photo Capture'),
            specs=[[{'type': 'indicator'}, {'type': 'bar'}]]
        )
        
        # Quality score gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=quality_metrics['avg_quality_score'],
            title={'text': "Avg Quality Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': ProgressCharts.COLORS['completed']},
                'steps': [
                    {'range': [0, 50], 'color': '#FFE5E5'},
                    {'range': [50, 75], 'color': '#FFD6AA'},
                    {'range': [75, 90], 'color': '#C9F0E5'},
                    {'range': [90, 100], 'color': '#B8E6D5'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 2},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ), row=1, col=1)
        
        # GPS and Photo rates
        fig.add_trace(go.Bar(
            x=['GPS Captured', 'Photo Attached'],
            y=[quality_metrics['gps_capture_rate'], quality_metrics['photo_attach_rate']],
            marker_color=[ProgressCharts.COLORS['completed'], ProgressCharts.COLORS['primary']],
            text=[f"{quality_metrics['gps_capture_rate']}%", f"{quality_metrics['photo_attach_rate']}%"],
            textposition='auto'
        ), row=1, col=2)
        
        fig.update_layout(
            height=350,
            showlegend=False
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_logistics_status_chart(logistics):
        """Create logistics and field conditions status chart"""
        categories = ['Transport', 'Network', 'Devices', 'Power']
        good = [logistics['transport_good'], logistics['network_good'], 
                logistics['devices_ok'], logistics['power_good']]
        poor = [logistics['transport_poor'], logistics['network_poor'], 
                logistics['devices_faulty'] + logistics['devices_replaced'], logistics['power_poor']]
        none_vals = [logistics['transport_none'], logistics['network_none'], 0, 0]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Good/OK', x=categories, y=good, 
                            marker_color=ProgressCharts.COLORS['completed']))
        fig.add_trace(go.Bar(name='Poor/Faulty', x=categories, y=poor, 
                            marker_color=ProgressCharts.COLORS['warning']))
        fig.add_trace(go.Bar(name='None', x=categories, y=none_vals, 
                            marker_color=ProgressCharts.COLORS['danger']))
        
        fig.update_layout(
            title='Logistics & Field Conditions Status',
            xaxis_title='Category',
            yaxis_title='Count',
            barmode='stack',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_supervisor_review_chart(supervisor_data):
        """Create supervisor review summary chart"""
        supervisor_data_reset = supervisor_data.reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=supervisor_data_reset['supervisor_name'],
            y=supervisor_data_reset['total_reviews'],
            name='Total Reviews',
            marker_color=ProgressCharts.COLORS['primary'],
            text=supervisor_data_reset['total_reviews'],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=supervisor_data_reset['supervisor_name'],
            y=supervisor_data_reset['approved'],
            name='Approved',
            marker_color=ProgressCharts.COLORS['completed'],
            text=supervisor_data_reset['approved'],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Supervisor Review Summary',
            xaxis_title='Supervisor',
            yaxis_title='Count',
            barmode='group',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_ea_completion_map(province_ea_data):
        """Create enumeration area completion by province"""
        province_ea_reset = province_ea_data.reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=province_ea_reset['province'],
            y=province_ea_reset['ea_completion_percentage'],
            marker_color=ProgressCharts.COLORS['completed'],
            text=[f"{val}%" for val in province_ea_reset['ea_completion_percentage']],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='% of Enumeration Areas Completed by Province',
            xaxis_title='Province',
            yaxis_title='Completion Rate (%)',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_data_error_rate_chart(interviewer_data):
        """Create data error rate by team chart"""
        interviewer_data_reset = interviewer_data.reset_index()
        team_errors = interviewer_data_reset.groupby('team').agg({
            'incomplete_forms': 'sum',
            'rejected_forms': 'sum',
            'total_surveys': 'sum'
        }).reset_index()
        
        team_errors['error_rate'] = round(
            ((team_errors['incomplete_forms'] + team_errors['rejected_forms']) / 
             team_errors['total_surveys'] * 100), 2
        )
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=team_errors['team'],
            y=team_errors['error_rate'],
            marker_color=ProgressCharts.COLORS['warning'],
            text=[f"{val}%" for val in team_errors['error_rate']],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Data Error Rate by Team',
            xaxis_title='Team',
            yaxis_title='Error Rate (%)',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_household_status_chart(ea_stats):
        """Create household status breakdown chart"""
        total_hh = ea_stats['ea_total_households'].sum()
        completed_hh = ea_stats['ea_completed'].sum()
        refused_hh = ea_stats['ea_refused'].sum()
        not_found_hh = ea_stats['ea_not_found'].sum()
        remaining_hh = ea_stats['ea_remaining'].sum()
        
        fig = go.Figure(data=[go.Pie(
            labels=['Completed', 'Refused', 'Not Found', 'Remaining'],
            values=[completed_hh, refused_hh, not_found_hh, remaining_hh],
            marker=dict(colors=[
                ProgressCharts.COLORS['completed'],
                ProgressCharts.COLORS['danger'],
                ProgressCharts.COLORS['warning'],
                ProgressCharts.COLORS['pending']
            ]),
            textinfo='label+percent+value',
            hole=0.3
        )])
        
        fig.update_layout(
            title=f'Household Status Breakdown (Total: {total_hh:,} HH)',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_interviewer_daily_progress_chart(interviewer_data):
        """Create average daily progress per interviewer"""
        interviewer_data_reset = interviewer_data.reset_index()
        top_performers = interviewer_data_reset.nlargest(15, 'avg_daily_progress')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_performers['interviewer_name'],
            y=top_performers['avg_daily_progress'],
            marker_color=ProgressCharts.COLORS['primary'],
            text=[f"{val:.1f}" for val in top_performers['avg_daily_progress']],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Average Daily Progress per Enumerator (HH/day)',
            xaxis_title='Enumerator',
            yaxis_title='Households per Day',
            height=400,
            xaxis_tickangle=-45
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_survey_solutions_sync_chart(sync_summary):
        """Create Survey Solutions sync status chart"""
        fig = go.Figure(data=[go.Pie(
            labels=['Synced', 'Pending', 'Failed'],
            values=[sync_summary['synced'], sync_summary['pending'], sync_summary['failed']],
            marker=dict(colors=[
                ProgressCharts.COLORS['completed'],
                ProgressCharts.COLORS['warning'],
                ProgressCharts.COLORS['danger']
            ]),
            textinfo='label+percent+value',
            hole=0.4
        )])
        
        fig.update_layout(
            title=f'Survey Solutions Sync Status (Rate: {sync_summary["sync_rate"]}%)',
            height=400,
            annotations=[dict(text=f'{sync_summary["sync_rate"]}%<br>Synced', 
                            x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_ss_interview_status_chart(status_counts):
        """Create Survey Solutions interview status distribution chart"""
        # Shorten status names for display
        status_map = {
            'Completed': 'Completed',
            'InterviewerAssigned': 'Assigned',
            'RejectedBySupervisor': 'Rej. by Sup.',
            'ApprovedBySupervisor': 'App. by Sup.',
            'RejectedByHeadquarters': 'Rej. by HQ',
            'ApprovedByHeadquarters': 'App. by HQ'
        }
        
        labels = [status_map.get(k, k) for k in status_counts.keys()]
        values = list(status_counts.values())
        
        fig = go.Figure(data=[go.Bar(
            x=labels,
            y=values,
            marker_color=ProgressCharts.COLORS['primary'],
            text=values,
            textposition='auto'
        )])
        
        fig.update_layout(
            title='Survey Solutions Interview Status',
            xaxis_title='Status',
            yaxis_title='Count',
            height=400,
            xaxis_tickangle=-45
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_device_sync_performance_chart(device_sync_data):
        """Create device/interviewer sync performance chart"""
        device_sync_reset = device_sync_data.reset_index()
        top_performers = device_sync_reset.nlargest(15, 'sync_success_rate')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_performers['interviewer_name'],
            y=top_performers['sync_success_rate'],
            name='Sync Success Rate',
            marker_color=ProgressCharts.COLORS['completed'],
            text=[f"{val:.1f}%" for val in top_performers['sync_success_rate']],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Tablet Sync Success Rate by Enumerator (Top 15)',
            xaxis_title='Enumerator',
            yaxis_title='Success Rate (%)',
            height=400,
            xaxis_tickangle=-45,
            yaxis=dict(range=[0, 100])
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_validation_errors_chart(device_sync_data):
        """Create chart showing validation errors by interviewer"""
        device_sync_reset = device_sync_data.reset_index()
        # Get interviewers with most validation errors
        top_errors = device_sync_reset.nlargest(15, 'total_validation_errors')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_errors['interviewer_name'],
            y=top_errors['total_validation_errors'],
            marker_color=ProgressCharts.COLORS['danger'],
            text=top_errors['total_validation_errors'],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Survey Solutions Validation Errors by Enumerator',
            xaxis_title='Enumerator',
            yaxis_title='Total Validation Errors',
            height=400,
            xaxis_tickangle=-45
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
