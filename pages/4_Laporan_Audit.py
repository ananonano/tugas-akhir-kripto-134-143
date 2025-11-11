import streamlit as st
from database import get_user_history
import pandas as pd
import json
from collections import defaultdict

st.set_page_config(page_title="Laporan Audit", layout="wide")

if not st.session_state.get('logged_in', False):
    st.error("Anda harus login untuk mengakses halaman ini.")
    st.stop()

st.title(f"Laporan Audit Keuangan {st.session_state['username']}")

user_id = st.session_state['user_id']
history_data = get_user_history(user_id)

total_pemasukan = 0.0
total_pengeluaran = 0.0
linked_activities_map = defaultdict(list)
linked_log_ids = set()
other_logs = []

if not history_data:
    st.info("Anda belum memiliki riwayat aktivitas.")
    st.header("Ringkasan Keuangan")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemasukan", "Rp 0,00")
    col2.metric("Total Pengeluaran", "Rp 0,00")
    col3.metric("Saldo Akhir", "Rp 0,00")
    st.divider()
    st.info("Log aktivitas Anda akan muncul di sini setelah Anda melakukan aksi.")
    
else:
    # PASS 1: Hitung Total dan Bangun Peta Tautan
    for entry in history_data:
        action = entry['action']
        details_str = entry['details']
        entry_id = entry['id'] 
        
        if action == "Catat Transaksi":
            try:
                data = json.loads(details_str)
                nominal = float(data.get('nominal', 0))
                if data.get('tipe') == 'Pemasukan':
                    total_pemasukan += nominal
                elif data.get('tipe') == 'Pengeluaran':
                    total_pengeluaran += nominal
            except (json.JSONDecodeError, TypeError, ValueError):
                pass 
        
        try:
            data = json.loads(details_str)
            linked_tx_id = data.get('linked_tx_id')
            
            if linked_tx_id is not None:
                linked_log_ids.add(entry_id) 
                ts = entry['timestamp'].strftime('%Y-%m-%d %H:%M')
                display_text = f"[{ts}] "
                
                # PERBAIKAN IKON
                if action == "CAST-128 Enkripsi Struk":
                    display_text += f"📄 Struk Dienkripsi: {data.get('file_name', 'N/A')} (Hint: {data.get('key_hint', 'N/A')})"
                elif action == "CAST-128 Dekripsi Struk":
                    display_text += f"🔓 Struk Didekripsi: {data.get('file_name', 'N/A')}"
                elif action == "PVD Hide":
                    display_text += f"🖼️ Gambar Disisipi: {data.get('file_name', 'N/A')} (Hint: {data.get('message_hint', 'N/A')})"
                elif action == "PVD Reveal":
                    display_text += f"🔎 Gambar Diekstrak: {data.get('file_name', 'N/A')} (Hint: {data.get('revealed_hint', 'N/A')})"
                else:
                    display_text += f"Aktivitas: {action}"
                
                linked_activities_map[linked_tx_id].append(display_text)
            
            else:
                if action not in ["Catat Transaksi"]:
                    other_logs.append(entry)
                
        except (json.JSONDecodeError, TypeError, ValueError):
            if action not in ["Catat Transaksi"]:
                other_logs.append(entry)
            
    # Tampilkan Ringkasan
    saldo_akhir = total_pemasukan - total_pengeluaran
    st.header("Ringkasan Keuangan")
    st.caption("Dihitung berdasarkan log transaksi yang tersimpan di database.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemasukan", f"Rp {total_pemasukan:,.2f}", delta=total_pemasukan, delta_color="normal")
    col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.2f}", delta=-total_pengeluaran, delta_color="normal")
    col3.metric("Saldo Akhir", f"Rp {saldo_akhir:,.2f}", delta=saldo_akhir, delta_color="normal")
    st.divider()

    # PASS 2: Tampilkan Log
    st.header("Detail Log Transaksi (Tergrup)")
    
    transaction_logs = [e for e in history_data if e['action'] == "Catat Transaksi"]
    st.write(f"Menampilkan **{len(transaction_logs)}** transaksi terkelompok (dari total {len(history_data)} log):")

    if not transaction_logs:
        st.info("Belum ada transaksi yang dicatat.")

    for tx in transaction_logs:
        try:
            data = json.loads(tx['details'])
            tipe = data.get('tipe')
            nominal_str = f"Rp {float(data.get('nominal', 0)):,.2f}"
            keterangan = data.get('keterangan')
            tx_id = tx['id']
            
            # PERBAIKAN IKON
            expander_icon = "🟢" if tipe == "Pemasukan" else "🔴"
            expander_title = f"{expander_icon} **{tx['timestamp'].strftime('%Y-%m-%d %H:%M')}** - **{tipe}** - **{nominal_str}** (ID: {tx_id})"

            with st.expander(expander_title):
                st.markdown(f"**Keterangan:** {keterangan}")
                
                if tx_id in linked_activities_map:
                    st.divider()
                    st.markdown("**Aktivitas Terkait:**")
                    sorted_activities = sorted(linked_activities_map[tx_id])
                    for activity_str in sorted_activities:
                        st.text(f"  {activity_str}") # <-- Hanya menampilkan teks
                else:
                    st.caption("Tidak ada file/gambar yang ditautkan ke transaksi ini.")

        except (json.JSONDecodeError, TypeError, ValueError, KeyError):
             st.error(f"Log Transaksi (ID: {tx.get('id', 'N/A')}) rusak atau format lama.")

    # BAGIAN 4: Menampilkan Log Lainnya
    if other_logs:
        st.divider()
        st.header("Log Aktivitas Lainnya (Tidak Terkait)")
        other_logs.sort(key=lambda x: x['timestamp'], reverse=True)
        
        for entry in other_logs:
            with st.expander(f"**{entry['timestamp'].strftime('%Y-%m-%d %H:%M')}** - **{entry['action']}**"):
                try:
                    data = json.loads(entry['details'])
                    st.json(data)
                except (json.JSONDecodeError, TypeError, ValueError):
                    st.text(f"Detail:\n{entry['details']}")

    if st.checkbox("Tampilkan sebagai tabel (data mentah asli)"):
        st.write("Data mentah ini *sebelum* pengelompokan:")
        df = pd.DataFrame(history_data)
        st.dataframe(df)
        
if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.session_state['user_id'] = 0
    st.rerun()